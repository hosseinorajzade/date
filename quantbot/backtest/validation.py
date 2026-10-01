"""Robustness diagnostics: parameter sensitivity, cost stress, regime split, cross-asset runs."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..strategies.base import Strategy
from ..strategies.registry import make
from .costs import CostModel
from .engine import EngineConfig
from .metrics import daily_returns, sharpe
from .runner import SliceRunner, full_stats, quick_stats
from .walkforward import ckey


def sensitivity(family: type[Strategy], params: dict, runner: SliceRunner, signals: dict[tuple, pd.DataFrame],
                a: int = 0, b: int | None = None) -> dict:
    """Run the chosen config and every one-step neighbour on the same span."""
    rows = []
    for tag, p in [("chosen", params)] + [("neighbour", q) for q in family.neighbors(params)]:
        sig = signals.get(ckey(p))
        if sig is None:
            sig = make(family.name, **p).generate(runner.df)
        qs = quick_stats(runner.run(sig, a, b))
        rows.append({"role": tag, "params": p, **qs})
    t = pd.DataFrame(rows)
    nb = t[t["role"] == "neighbour"]
    chosen_sr = float(t.loc[t["role"] == "chosen", "sharpe"].iloc[0])
    return {
        "table": t,
        "share_neighbours_positive": float((nb["sharpe"] > 0).mean()) if len(nb) else float("nan"),
        "median_neighbour_sharpe": float(nb["sharpe"].median()) if len(nb) else float("nan"),
        "chosen_sharpe": chosen_sr,
        "neighbour_to_chosen_ratio": float(nb["sharpe"].median() / chosen_sr) if len(nb) and chosen_sr > 0 else float("nan"),
    }


def cost_stress(runner: SliceRunner, sig: pd.DataFrame, a: int, b: int, multipliers=(1.0, 1.5, 2.0)) -> pd.DataFrame:
    rows = []
    for m in multipliers:
        cfg = runner.cfg.with_costs(runner.cfg.costs.stressed(m))
        res = runner.run(sig, a, b, cfg=cfg)
        rows.append({"cost_multiplier": m, **full_stats(res)})
    return pd.DataFrame(rows)


def label_regimes(close: pd.Series) -> pd.DataFrame:
    """Daily regime labels from TRAILING information only (so labels are knowable at the time)."""
    d = close.resample("1D").last().dropna()
    ret90 = d / d.shift(90) - 1.0
    vol30 = np.log(d).diff().rolling(30).std()
    hv = vol30 > vol30.expanding(min_periods=60).median()  # expanding median: no future information
    trend = pd.Series("sideways", index=d.index)
    trend[ret90 > 0.25] = "bull"
    trend[ret90 < -0.25] = "bear"
    trend[ret90.isna()] = "warmup"
    vol = pd.Series(np.where(hv, "high_vol", "low_vol"), index=d.index)
    vol[vol30.isna()] = "warmup"
    return pd.DataFrame({"trend": trend, "vol": vol})


def regime_breakdown(equity: pd.Series, close: pd.Series) -> pd.DataFrame:
    dr = daily_returns(equity)
    lab = label_regimes(close).shift(1)  # label known at the previous close
    j = pd.concat([dr, lab], axis=1, join="inner").dropna()
    rows = []
    for col in ("trend", "vol"):
        for name, g in j.groupby(col):
            if name == "warmup":
                continue
            rows.append({"dimension": col, "regime": name, "days": int(len(g)),
                         "mean_daily_ret_bps": float(g["ret"].mean() * 1e4), "sharpe": sharpe(g["ret"]),
                         "total_return": float((1 + g["ret"]).prod() - 1)})
    return pd.DataFrame(rows)


def placebo_test(runner: SliceRunner, sig: pd.DataFrame, a: int, b: int, n_shifts: int = 200, min_shift_bars: int = 24 * 7,
                 seed: int = 0) -> dict:
    """Time-shift permutation test.

    The signal series is circularly shifted by random offsets (>= 1 week) against the SAME price path, which keeps its
    entry/exit statistics, holding times, long/short mix and stop mechanics but destroys any alignment with prices.
    If the strategy's Sharpe is not clearly above this null distribution, its profit comes from the exit mechanics /
    market drift rather than from timing skill. (This test exposes artefacts such as discretisation-flattered stops.)
    """
    rng = np.random.default_rng(seed)
    n = b - a
    tgt, sd = sig["target"].to_numpy(), sig["stop_dist"].to_numpy()
    actual = quick_stats(runner.run(sig, a, b))["sharpe"]
    null = []
    for _ in range(n_shifts):
        k = int(rng.integers(min_shift_bars, max(n - min_shift_bars, min_shift_bars + 1)))
        idx = (np.arange(a, b) - k) % n + a  # shift inside the evaluation span so no future data enters
        shifted = (np.concatenate([[tgt[a - 1] if a > 0 else 0.0], tgt[idx]])[1:], sd[idx])
        null.append(quick_stats(runner.run((np.concatenate([tgt[:a], shifted[0]]), np.concatenate([sd[:a], shifted[1]])), a, b))["sharpe"])
    null = np.array([x for x in null if not np.isnan(x)])
    return {"actual_sharpe": actual, "placebo_mean": float(null.mean()), "placebo_p95": float(np.percentile(null, 95)),
            "placebo_std": float(null.std(ddof=1)), "p_value": float((np.sum(null >= actual) + 1) / (len(null) + 1)),
            "n_shifts": int(len(null))}
