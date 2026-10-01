"""Helpers to run the engine on slices of a longer, continuously computed signal series."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .engine import BacktestResult, EngineConfig, run_backtest
from .metrics import daily_returns, sharpe, summarize


class SliceRunner:
    """Holds OHLC + per-bar funding; runs a signal frame over [a, b) with the correct carried-in decision."""

    def __init__(self, df: pd.DataFrame, funding_per_bar: np.ndarray | float, cfg: EngineConfig):
        self.df, self.cfg = df, cfg
        self.funding = np.full(len(df), float(funding_per_bar)) if np.isscalar(funding_per_bar) \
            else np.asarray(funding_per_bar, dtype=float)

    def run(self, sig: pd.DataFrame | tuple[np.ndarray, np.ndarray], a: int = 0, b: int | None = None,
            cfg: EngineConfig | None = None) -> BacktestResult:
        b = len(self.df) if b is None else b
        tgt, sd = (sig["target"].to_numpy(), sig["stop_dist"].to_numpy()) if isinstance(sig, pd.DataFrame) else sig
        it = float(tgt[a - 1]) if a > 0 else 0.0
        isd = float(sd[a - 1]) if a > 0 else np.nan
        return run_backtest(self.df.iloc[a:b], tgt[a:b], sd[a:b], cfg or self.cfg, self.funding[a:b], it, isd)


def trade_returns(res: BacktestResult) -> np.ndarray:
    """Per-trade net return as a fraction of equity at entry (for trade-sequence Monte Carlo)."""
    tr = res.trades
    if tr.empty:
        return np.array([])
    eq_prev = res.equity.shift(1).fillna(res.config.initial_equity).to_numpy()
    return tr["net"].to_numpy() / eq_prev[tr["entry_idx"].to_numpy()]


def quick_stats(res: BacktestResult) -> dict:
    dr = daily_returns(res.equity)
    return {"sharpe": sharpe(dr), "ret": float(res.equity.iloc[-1] / res.config.initial_equity - 1),
            "n_trades": int(len(res.trades))}


def full_stats(res: BacktestResult) -> dict:
    s = summarize(res.equity, res.trades, res.config.initial_equity)
    s["kill_events"], s["daily_halts"] = res.n_kill_events, res.n_daily_halts
    return s
