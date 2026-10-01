"""Rolling walk-forward optimisation (WFO).

For each window: choose parameters on the TRAIN span only (plateau-smoothed Sharpe: a config's score is
the mean of its own and its neighbours' scores, so isolated peaks lose to broad plateaus), then trade the
following TEST span with those frozen parameters. Test spans are stitched into one genuinely
out-of-sample equity curve. Every window starts flat with equity 1.0 (conservative: no carried-over
position or compounding advantage).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..strategies.base import Strategy
from ..strategies.registry import make
from .engine import EngineConfig
from .metrics import daily_returns, max_drawdown, profit_factor, sharpe, sortino
from .runner import SliceRunner

FLOOR = -5.0  # objective for configs with too few trades to score


def ckey(p: dict) -> tuple:
    return tuple(sorted(p.items()))


@dataclass
class WFResult:
    windows: pd.DataFrame
    equity: pd.Series
    trades: pd.DataFrame
    summary: dict


def score(res, min_trades: int) -> float:
    if len(res.trades) < min_trades:
        return FLOOR
    s = sharpe(daily_returns(res.equity))
    return FLOOR if np.isnan(s) else float(s)


def plateau_scores(scores: dict[tuple, float], family: type[Strategy]) -> dict[tuple, float]:
    out = {}
    for k in scores:
        p = dict(k)
        vals = [scores[k]] + [scores[ckey(nb)] for nb in family.neighbors(p) if ckey(nb) in scores]
        out[k] = float(np.mean(vals))
    return out


def walk_forward(df: pd.DataFrame, funding: np.ndarray, family: type[Strategy], cfg: EngineConfig,
                 train_days: int, test_days: int, step_days: int, bars_per_day: float,
                 min_train_trades: int = 10, signals: dict[tuple, pd.DataFrame] | None = None) -> WFResult:
    configs = family.configs()
    if signals is None:
        signals = {ckey(p): make(family.name, **p).generate(df) for p in configs}
    ecfg = EngineConfig(**{**cfg.__dict__, "trailing": family.trail})
    runner = SliceRunner(df, funding, ecfg)
    tb, sb, stb = (int(round(x * bars_per_day)) for x in (train_days, test_days, step_days))
    rows, eq_parts, trade_parts = [], [], []
    stitched_end = 1.0
    a = 0
    k = 0
    while a + tb + sb <= len(df):
        b, c = a + tb, a + tb + sb
        scores = {ckey(p): score(runner.run(signals[ckey(p)], a, b), min_train_trades) for p in configs}
        smooth = plateau_scores(scores, family)
        best = max(smooth, key=lambda x: (smooth[x], scores[x]))
        res = runner.run(signals[best], b, c)
        ret = float(res.equity.iloc[-1] - 1.0)
        rows.append({"window": k, "train_start": df.index[a], "test_start": df.index[b], "test_end": df.index[c - 1],
                     "params": dict(best), "train_sharpe": scores[best], "train_plateau": smooth[best],
                     "oos_return": ret, "oos_sharpe": sharpe(daily_returns(res.equity)),
                     "oos_trades": int(len(res.trades)), "oos_mdd": max_drawdown(res.equity.to_numpy())})
        eq_parts.append(res.equity * stitched_end)
        stitched_end = float(eq_parts[-1].iloc[-1])
        t = res.trades.copy()
        if len(t):
            t["window"] = k
            t["entry_idx"] += b
            t["exit_idx"] += b
            trade_parts.append(t)
        a += stb
        k += 1
    if not rows:
        raise ValueError("not enough data for a single walk-forward window")
    win = pd.DataFrame(rows)
    # test spans can overlap when step < test; keep the first occurrence of each timestamp so the curve is well defined
    eq = pd.concat(eq_parts)
    eq = eq[~eq.index.duplicated(keep="first")]
    trades = pd.concat(trade_parts, ignore_index=True) if trade_parts else pd.DataFrame()
    dr = daily_returns(eq)
    n_params = len({ckey(p) for p in win["params"]})
    summary = {
        "n_windows": int(len(win)), "positive_window_share": float((win["oos_return"] > 0).mean()),
        "oos_sharpe": sharpe(dr), "oos_sortino": sortino(dr), "oos_mdd": max_drawdown(eq.to_numpy()),
        "oos_net_return": float(eq.iloc[-1] / eq.iloc[0] - 1) if len(eq) else float("nan"),
        "oos_trades": int(len(trades)),
        "oos_profit_factor": profit_factor(trades["net"]) if len(trades) else float("nan"),
        "distinct_param_sets_chosen": n_params,
        "median_train_sharpe": float(win["train_sharpe"].median()),
    }
    return WFResult(win, eq, trades, summary)
