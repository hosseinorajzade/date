"""Markdown backtest reports built from the artefacts the pipeline writes (JSON/CSV/PNG)."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def _fmt(x, nd=3):
    if isinstance(x, bool):
        return "yes" if x else "no"
    if isinstance(x, (int,)):
        return str(x)
    if isinstance(x, float):
        return "n/a" if pd.isna(x) else (f"{x:.{nd}f}" if abs(x) < 1e6 else f"{x:.3g}")
    return str(x)


def md_table(df: pd.DataFrame, nd: int = 3) -> str:
    if df.empty:
        return "_(none)_\n"
    cols = list(df.columns)
    out = ["| " + " | ".join(map(str, cols)) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(_fmt(r[c], nd) for c in cols) + " |")
    return "\n".join(out) + "\n"


def family_report(fdir: Path, gates: dict | None = None) -> str:
    name = fdir.name
    L = [f"## Family `{name}`\n"]
    res_path = fdir / "holdout_result.json"
    if gates is not None:
        L.append("### Research gates (train+validation only)\n")
        L.append(md_table(pd.DataFrame([{"gate": k, "value": v[0], "threshold": v[1], "pass": v[2]} for k, v in gates.items()])))
    if (fdir / "research_grid.csv").exists():
        g = pd.read_csv(fdir / "research_grid.csv")
        L.append("### Research grid (every configuration tried; all count as trials)\n")
        L.append(md_table(g.sort_values("research_sharpe", ascending=False).head(10)))
        L.append(f"_{len(g)} configurations in total; top 10 by research Sharpe shown. "
                 f"Median research Sharpe {g['research_sharpe'].median():.2f}._\n")
    if (fdir / "walkforward_windows.csv").exists():
        w = pd.read_csv(fdir / "walkforward_windows.csv")
        L.append("### Walk-forward (re-optimised each window; out-of-sample test spans)\n")
        L.append(md_table(w[["test_start", "test_end", "params", "train_sharpe", "oos_return", "oos_sharpe", "oos_trades", "oos_mdd"]]))
        L.append("![wfo](research_wfo.png)\n")
    if (fdir / "sensitivity.csv").exists():
        L.append("### Parameter sensitivity (chosen config vs one-step neighbours, research period)\n")
        L.append(md_table(pd.read_csv(fdir / "sensitivity.csv")))
    if res_path.exists():
        r = json.loads(res_path.read_text())
        h, s = r["holdout"], r["stressed"]
        L.append("### HOLD-OUT result (single look, frozen parameters, net of costs)\n")
        L.append(f"Frozen params: `{r['params']}`  |  period {h['start']} → {h['end']} ({h['years']} y)  |  "
                 f"buy&hold over the same span: {r['buy_and_hold_return']:+.1%}\n")
        keys = ["net_return", "cagr", "sharpe", "sortino", "max_drawdown", "calmar", "profit_factor", "win_rate", "n_trades",
                "avg_r", "avg_bars_held", "ann_vol", "fees_paid_pct", "funding_paid_pct", "stop_exits", "kill_events", "daily_halts"]
        L.append(md_table(pd.DataFrame([{"metric": k, "1.0x costs": h.get(k), "1.5x costs": s.get(k)} for k in keys])))
        L.append("### Acceptance criteria\n")
        a = pd.DataFrame(r["acceptance"])
        a["pass"] = a["pass"].map({True: "PASS", False: "FAIL"})
        L.append(md_table(a))
        L.append(f"**Verdict: {'ACCEPTED' if r['accepted'] else 'NOT ACCEPTED'}**\n")
        d = r["dsr"]
        L.append(f"### Multiple-testing correction\nN_raw={d['n_raw']} configs tried, N_eff={d['n_effective']:.1f}. Expected-max-Sharpe benchmark "
                 f"SR0={d['sr0_ann']:.2f}/yr (null sampling variance); hold-out SR={h['sharpe']:.2f}; DSR={d['dsr']:.3f}. "
                 f"Strict variant (empirical cross-trial variance, raw N): SR0={d['sr0_ann_strict']:.2f}/yr, DSR={d['dsr_strict']:.3f}. "
                 f"Undeflated PSR(SR>0)={d['psr_vs_zero']:.3f}; skew={d['skew']:.2f}, kurtosis={d['kurtosis']:.1f}, n={d['n_obs']} days.\n")
        L.append("### Cost stress\n")
        L.append(md_table(pd.read_csv(fdir / "holdout_cost_stress.csv")[["cost_multiplier", "net_return", "sharpe", "sortino", "max_drawdown", "profit_factor", "n_trades"]]))
        mc, bs, pl = r["monte_carlo"], r["bootstrap"], r.get("placebo", {})
        L.append("### Monte Carlo / bootstrap / placebo\n")
        L.append(f"* Trade-sequence MC ({mc.get('n_trades')} trades, resampled): P(profit)={mc.get('p_profit', float('nan')):.3f}, "
                 f"final return p05/p50/p95 = {mc.get('final_return_p05', float('nan')):+.2f}/{mc.get('final_return_p50', float('nan')):+.2f}/"
                 f"{mc.get('final_return_p95', float('nan')):+.2f}, max-DD p50/p95/p99 = {mc.get('mdd_p50', float('nan')):.2f}/"
                 f"{mc.get('mdd_p95', float('nan')):.2f}/{mc.get('mdd_p99', float('nan')):.2f}, P(MDD>20%)={mc.get('p_mdd_gt_20', float('nan')):.3f}")
        L.append(f"* Stationary bootstrap of daily returns: Sharpe p05/p50/p95 = {bs['sharpe_p05']:.2f}/{bs['sharpe_p50']:.2f}/{bs['sharpe_p95']:.2f}; "
                 f"P(Sharpe>0)={bs['p_sharpe_gt_0']:.3f}")
        if pl:
            L.append(f"* Time-shift placebo ({pl['n_shifts']} shifts): actual Sharpe {pl['actual_sharpe']:.2f} vs placebo mean {pl['placebo_mean']:.2f} "
                     f"(p95 {pl['placebo_p95']:.2f}); p-value {pl['p_value']:.3f}")
        L.append(f"* 90-day windows positive: {r['windows_positive_share']:.2f} of {r['n_windows']}\n")
        L.append("### Hold-out by market regime (labels from trailing data only)\n")
        L.append(md_table(pd.read_csv(fdir / "holdout_regimes.csv")))
        if r["cross_asset_holdout"]:
            L.append("### Same frozen parameters on other assets (hold-out span; NOT re-fit)\n")
            L.append(md_table(pd.DataFrame(r["cross_asset_holdout"]).T.reset_index().rename(columns={"index": "asset"})))
        L.append("![holdout](holdout.png)\n")
    return "\n".join(L)


def run_report(out_dir: str | Path, title: str, preface: str = "") -> Path:
    out = Path(out_dir)
    summ = json.loads((out / "summary.json").read_text())
    L = [f"# {title}\n", preface, ""]
    ni = summ["n_trials"]
    L.append(f"Trials registered: **{ni['n_trials_raw']}** configurations (effective independent ≈ {ni['n_trials_effective']:.1f}); "
             f"by family: {ni['by_family']}\n")
    rows = []
    for fam, r in summ["results"].items():
        if r["stage"] == "holdout":
            h = r["holdout"]
            rows.append({"family": fam, "stage": "hold-out", "params": str(r["params"]), "net": h["net_return"], "sharpe": h["sharpe"],
                         "sortino": h["sortino"], "mdd": h["max_drawdown"], "PF": h["profit_factor"], "trades": h["n_trades"],
                         "DSR": r["dsr"]["dsr"], "accepted": r["accepted"]})
        else:
            rows.append({"family": fam, "stage": "rejected at research", "params": str(r["params"]), "net": None, "sharpe": None,
                         "sortino": None, "mdd": None, "PF": None, "trades": None, "DSR": None, "accepted": False})
    L.append("## Summary\n")
    L.append(md_table(pd.DataFrame(rows)))
    for fam, r in summ["results"].items():
        L.append(family_report(out / fam, r.get("gates")))
    p = out / "report.md"
    p.write_text("\n".join(L))
    return p
