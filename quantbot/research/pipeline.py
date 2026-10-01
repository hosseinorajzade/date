"""End-to-end research pipeline.

Stage 1 (research data only = train+validation): audit -> trial registration -> walk-forward -> sensitivity -> gates
Stage 2 (hold-out, ONE look per family, only for families that pass the gates): frozen params -> metrics, cost stress,
         Monte Carlo, bootstrap, regimes, cross-asset -> deflated Sharpe with ALL trials -> acceptance verdict.
Stage 1 is run for every family BEFORE any hold-out look so the multiple-testing denominator is final and identical
for all families.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd

from ..backtest import stats
from ..backtest.acceptance import evaluate_acceptance
from ..backtest.costs import CostModel
from ..backtest.engine import EngineConfig
from ..backtest.metrics import daily_returns, sharpe, summarize, window_returns
from ..backtest.runner import SliceRunner, full_stats, trade_returns
from ..backtest.trials import TrialRegistry, config_key
from ..backtest.validation import cost_stress, placebo_test, regime_breakdown, sensitivity
from ..backtest.walkforward import ckey, plateau_scores, walk_forward
from ..config import bars_per_day, timeframe_to_minutes
from ..data.splits import DataSplit, HoldoutVault
from ..data.store import funding_per_bar
from ..reporting import journal
from ..reporting.plots import equity_report_png
from ..strategies.audit import check_no_lookahead
from ..strategies.base import Strategy
from ..strategies.registry import FAMILIES, make

# data_provider(symbol) -> (clean_df, raw_funding_series_or_None)
DataProvider = Callable[[str], tuple[pd.DataFrame, "pd.Series | None"]]


@dataclass
class FamilyResearch:
    family: str
    chosen: dict
    gates: dict
    gate_passed: bool
    wf_summary: dict
    sens: dict
    research_stats: dict
    signals: dict
    notes: list[str]


def _jsonable(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, (pd.Timestamp,)):
        return str(o)
    if isinstance(o, pd.DataFrame):
        return json.loads(o.to_json(orient="records", date_format="iso"))
    raise TypeError(type(o))


def _fund(cfg, df, funding):
    return funding_per_bar(funding, df.index, timeframe_to_minutes(cfg["market"]["timeframe"]),
                           cfg["costs"]["funding_bps_per_8h"]).to_numpy()


def research_family(cfg: dict, name: str, df_all: pd.DataFrame, funding: pd.Series | None, split: DataSplit,
                    registry: TrialRegistry, out_dir: Path, run_audit: bool = True) -> FamilyResearch:
    fam = FAMILIES[name]
    bpd = bars_per_day(cfg["market"]["timeframe"])
    df = split.research(df_all)
    notes: list[str] = []
    if run_audit:
        s_mid = make(name, **fam.configs()[len(fam.configs()) // 2])
        if name == "ml_gbm":  # model refits are slow: audit a prefix here (tests/test_strategies.py audits more cuts)
            v = check_no_lookahead(s_mid, df.iloc[: 24 * 330], cut_points=[24 * 230, 24 * 280, 24 * 329])
        else:
            v = check_no_lookahead(s_mid, df, n_cuts=4)
        if v:
            raise RuntimeError(f"LOOK-AHEAD DETECTED in {name}: {v[:2]}")
        notes.append("look-ahead audit passed (truncation invariance)")
    base = EngineConfig.from_config(cfg, trailing=fam.trail)
    fund = _fund(cfg, df, funding)
    runner = SliceRunner(df, fund, base)
    configs = fam.configs()
    signals = {ckey(p): make(name, **p).generate(df) for p in configs}
    ntrain = int(df.index.searchsorted(split.train_end))
    rows = []
    for p in configs:  # trial registration: every config, over the full research span
        res = runner.run(signals[ckey(p)])
        dr = daily_returns(res.equity)
        registry.record(name, p, dr, note="research")
        tr = runner.run(signals[ckey(p)], 0, ntrain)
        va = runner.run(signals[ckey(p)], ntrain, len(df))
        rows.append({"params": p, "research_sharpe": sharpe(dr), "research_ret": float(res.equity.iloc[-1] - 1),
                     "research_trades": int(len(res.trades)), "train_sharpe": sharpe(daily_returns(tr.equity)),
                     "val_sharpe": sharpe(daily_returns(va.equity)), "val_ret": float(va.equity.iloc[-1] - 1),
                     "research_mdd": summarize(res.equity, res.trades)["max_drawdown"]})
    grid = pd.DataFrame(rows)
    wf_cfg = cfg["walkforward"]
    wf = walk_forward(df, fund, fam, base, wf_cfg["train_days"], wf_cfg["test_days"], wf_cfg["step_days"], bpd,
                      signals=signals)
    # frozen candidate for the hold-out: best plateau-smoothed research Sharpe (train+validation)
    scores = {ckey(r["params"]): (r["research_sharpe"] if r["research_trades"] >= 30 and not np.isnan(r["research_sharpe"]) else -5.0)
              for r in rows}
    smooth = plateau_scores(scores, fam)
    chosen = dict(max(smooth, key=lambda k: (smooth[k], scores[k])))
    sens = sensitivity(fam, chosen, runner, signals)
    chosen_res = runner.run(signals[ckey(chosen)])
    rs = full_stats(chosen_res)
    g = cfg["research_gates"]
    gates = {
        "wfo_sharpe": (wf.summary["oos_sharpe"], g["min_wfo_sharpe"], wf.summary["oos_sharpe"] >= g["min_wfo_sharpe"]),
        "wfo_positive_windows": (wf.summary["positive_window_share"], g["min_positive_windows"],
                                 wf.summary["positive_window_share"] >= g["min_positive_windows"]),
        "research_trades": (rs["n_trades"], g["min_trades"], rs["n_trades"] >= g["min_trades"]),
        "sensitivity_neighbours_positive": (sens["share_neighbours_positive"], g["min_sensitivity_positive"],
                                            sens["share_neighbours_positive"] >= g["min_sensitivity_positive"]),
    }
    passed = all(v[2] for v in gates.values())
    d = out_dir / name
    d.mkdir(parents=True, exist_ok=True)
    grid.to_csv(d / "research_grid.csv", index=False)
    wf.windows.to_csv(d / "walkforward_windows.csv", index=False)
    sens["table"].to_csv(d / "sensitivity.csv", index=False)
    equity_report_png(d / "research_wfo.png", wf.equity, f"{name}: stitched walk-forward OOS (research period)",
                      wf.windows.rename(columns={"oos_return": "ret"}))
    return FamilyResearch(name, chosen, gates, passed, wf.summary, {k: v for k, v in sens.items() if k != "table"},
                          rs, signals, notes)


def holdout_family(cfg: dict, fr: FamilyResearch, df_all: pd.DataFrame, funding: pd.Series | None, split: DataSplit,
                   vault: HoldoutVault, registry: TrialRegistry, out_dir: Path,
                   extra_assets: dict[str, tuple[pd.DataFrame, pd.Series | None]] | None = None) -> dict:
    name, params = fr.family, fr.chosen
    fam = FAMILIES[name]
    bpd = bars_per_day(cfg["market"]["timeframe"])
    ho_df = vault.open(df_all, name, params)  # logs + enforces one look per family
    start_pos = int(df_all.index.searchsorted(ho_df.index[0]))
    base = EngineConfig.from_config(cfg, trailing=fam.trail)
    fund = _fund(cfg, df_all, funding)
    runner = SliceRunner(df_all, fund, base)
    # signals are computed on the FULL history (indicators need the past); they are causal so this equals live use
    sig = make(name, **params).generate(df_all)
    res = runner.run(sig, start_pos)
    st = full_stats(res)
    acc = cfg["acceptance"]
    stress_res = runner.run(sig, start_pos, cfg=base.with_costs(base.costs.stressed(acc["stress_multiplier"])))
    stressed = full_stats(stress_res)
    stress_table = cost_stress(runner, sig, start_pos, len(df_all))
    dr = daily_returns(res.equity)
    win = window_returns(res.equity, acc["window_days"])
    # multiple-testing correction with the COMPLETE trial registry
    di = registry.deflation_inputs()
    n_eff = max(int(round(di["n_trials_effective"])), 1)
    d_pri = stats.deflated_sharpe(dr.to_numpy(), n_eff, di["trial_sr_var_null"])  # PRIMARY (gates acceptance)
    d_strict = stats.deflated_sharpe(dr.to_numpy(), di["n_trials_raw"], di["trial_sr_var_daily"])  # sensitivity
    dsr = {"dsr": d_pri["dsr"], "dsr_strict": d_strict["dsr"], "n_effective": di["n_trials_effective"],
           "n_raw": di["n_trials_raw"], "sr0_ann": d_pri["sr0_period"] * np.sqrt(365),
           "sr0_ann_strict": d_strict["sr0_period"] * np.sqrt(365), "psr_vs_zero": d_pri["psr_vs_zero"],
           "skew": d_pri["skew"], "kurtosis": d_pri["kurtosis"], "n_obs": d_pri["n_obs"]}
    mc = stats.trade_sequence_monte_carlo(trade_returns(res), cfg["monte_carlo"]["n_paths"], cfg["monte_carlo"]["seed"])
    boot = stats.bootstrap_sharpe_ci(dr.to_numpy(), seed=cfg["monte_carlo"]["seed"])
    verdict = evaluate_acceptance(acc, st, stressed, win["ret"].tolist(), dsr)
    regimes = regime_breakdown(res.equity, df_all["close"])
    placebo = placebo_test(runner, sig, start_pos, len(df_all), seed=cfg["monte_carlo"]["seed"])
    bh = df_all["close"].iloc[start_pos:]
    bh_eq = bh / bh.iloc[0]
    cross = {}
    for sym, (xdf, xfund) in (extra_assets or {}).items():
        xs = make(name, **params).generate(xdf)
        xr = SliceRunner(xdf, _fund(cfg, xdf, xfund), base)
        xstart = int(xdf.index.searchsorted(ho_df.index[0]))
        xres = xr.run(xs, xstart)
        cross[sym] = {k: full_stats(xres)[k] for k in ("net_return", "sharpe", "max_drawdown", "n_trades", "profit_factor")}
    d = out_dir / name
    equity_report_png(d / "holdout.png", res.equity, f"{name} {params}: HOLD-OUT (net of costs)", win, bh_eq,
                      stress_res.equity)
    stress_table.to_csv(d / "holdout_cost_stress.csv", index=False)
    regimes.to_csv(d / "holdout_regimes.csv", index=False)
    win.to_csv(d / "holdout_windows.csv", index=False)
    res.trades.to_csv(d / "holdout_trades.csv", index=False)
    dr.to_frame("ret").to_parquet(d / "holdout_daily_returns.parquet")
    out = {"family": name, "params": params, "holdout": st, "stressed": stressed, "dsr": dsr, "monte_carlo": mc,
           "bootstrap": boot, "placebo": placebo, "windows_positive_share": float((win["ret"] > 0).mean()), "n_windows": int(len(win)),
           "cross_asset_holdout": cross, "buy_and_hold_return": float(bh_eq.iloc[-1] - 1),
           "acceptance": verdict.as_rows(), "accepted": verdict.accepted}
    (d / "holdout_result.json").write_text(json.dumps(out, indent=2, default=_jsonable))
    return out


def run_all(cfg: dict, provider: DataProvider, out_dir: str | Path, families: list[str] | None = None,
            label: str = "run", journal_path: str | Path | None = None, run_audit: bool = True) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    journal_path = journal_path or out_dir / "journal.md"
    split = DataSplit.from_config(cfg)
    primary = cfg["market"]["primary"]
    df, funding = provider(primary)
    registry = TrialRegistry(out_dir)
    vault = HoldoutVault(split, out_dir / "holdout_log.json")
    names = families or list(FAMILIES)
    research = {}
    for n in names:  # ---- stage 1: every family on research data only
        research[n] = research_family(cfg, n, df, funding, split, registry, out_dir, run_audit)
        fr = research[n]
        journal.append(journal_path, f"[{label}] research: {n}",
                       f"chosen (plateau-smoothed research Sharpe): `{fr.chosen}`\n\n"
                       f"walk-forward OOS: {json.dumps(fr.wf_summary, default=_jsonable)}\n\n"
                       f"gates: {json.dumps({k: [float(v[0]), v[1], bool(v[2])] for k, v in fr.gates.items()})}\n\n"
                       f"**gate verdict: {'PASS -> hold-out eligible' if fr.gate_passed else 'FAIL -> hold-out not touched'}**")
    registry.flush()
    extra = {s: provider(s) for s in cfg["market"]["universe"] if s != primary}
    results = {}
    for n in names:  # ---- stage 2: hold-out, one look per eligible family, trial count now final
        fr = research[n]
        if not fr.gate_passed:
            results[n] = {"family": n, "params": fr.chosen, "accepted": False, "stage": "rejected_at_research",
                          "gates": {k: [float(v[0]), v[1], bool(v[2])] for k, v in fr.gates.items()}}
            continue
        r = holdout_family(cfg, fr, df, funding, split, vault, registry, out_dir, extra)
        r["stage"] = "holdout"
        results[n] = r
        h = r["holdout"]
        journal.append(journal_path, f"[{label}] HOLD-OUT: {n}",
                       f"params `{r['params']}`: net={h['net_return']:.3f} sharpe={h['sharpe']:.2f} sortino={h['sortino']:.2f} "
                       f"mdd={h['max_drawdown']:.3f} pf={h['profit_factor']:.2f} trades={h['n_trades']}; "
                       f"DSR={r['dsr']['dsr']:.3f} (strict {r['dsr']['dsr_strict']:.3f}); **accepted={r['accepted']}**")
    summary = {"label": label, "n_trials": registry.deflation_inputs(), "results": results}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, default=_jsonable))
    return summary
