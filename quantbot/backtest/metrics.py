"""Performance metrics. Sharpe/Sortino use DAILY (UTC) returns, annualised with 365 (crypto trades 24/7)."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

ANN = 365.0


def daily_returns(equity: pd.Series) -> pd.Series:
    """UTC-daily simple returns of an equity curve (first value is the base)."""
    eod = equity.resample("1D").last().dropna()
    first = equity.iloc[0]
    prev = eod.shift(1)
    prev.iloc[0] = first if len(eod) else np.nan
    return (eod / prev - 1.0).rename("ret")


def sharpe(ret: pd.Series | np.ndarray, ann: float = ANN) -> float:
    r = np.asarray(ret, dtype=float)
    r = r[~np.isnan(r)]
    if len(r) < 2:
        return float("nan")
    sd = r.std(ddof=1)
    return float(r.mean() / sd * math.sqrt(ann)) if sd > 0 else float("nan")


def sortino(ret: pd.Series | np.ndarray, ann: float = ANN, target: float = 0.0) -> float:
    r = np.asarray(ret, dtype=float)
    r = r[~np.isnan(r)]
    if len(r) < 2:
        return float("nan")
    dd = np.sqrt(np.mean(np.minimum(r - target, 0.0) ** 2))
    return float((r.mean() - target) / dd * math.sqrt(ann)) if dd > 0 else float("nan")


def max_drawdown(equity: pd.Series | np.ndarray) -> float:
    """Maximum peak-to-trough decline as a positive fraction (0.2 = 20%)."""
    e = np.asarray(equity, dtype=float)
    if len(e) == 0:
        return float("nan")
    peak = np.maximum.accumulate(e)
    return float(np.max(1.0 - e / peak))


def profit_factor(net_pnl: pd.Series | np.ndarray) -> float:
    x = np.asarray(net_pnl, dtype=float)
    gains, losses = x[x > 0].sum(), -x[x < 0].sum()
    if losses == 0:
        return float("inf") if gains > 0 else float("nan")
    return float(gains / losses)


def summarize(equity: pd.Series, trades: pd.DataFrame, initial_equity: float = 1.0) -> dict:
    """Headline statistics for one equity curve + trade list."""
    dr = daily_returns(equity)
    years = max((equity.index[-1] - equity.index[0]).total_seconds() / (365.25 * 86400), 1e-9)
    final = float(equity.iloc[-1] / initial_equity)
    out = {
        "start": str(equity.index[0].date()), "end": str(equity.index[-1].date()), "years": round(years, 3),
        "net_return": final - 1.0,
        "cagr": final ** (1 / years) - 1.0 if final > 0 else -1.0,
        "sharpe": sharpe(dr), "sortino": sortino(dr),
        "max_drawdown": max_drawdown(equity.to_numpy()),
        "ann_vol": float(dr.std(ddof=1) * math.sqrt(ANN)) if len(dr) > 1 else float("nan"),
        "n_trades": int(len(trades)),
    }
    out["calmar"] = out["cagr"] / out["max_drawdown"] if out["max_drawdown"] > 0 else float("nan")
    if len(trades):
        net = trades["net"].to_numpy() / initial_equity
        out.update(
            profit_factor=profit_factor(trades["net"]),
            win_rate=float((trades["net"] > 0).mean()),
            avg_r=float(trades["r_multiple"].mean()),
            avg_bars_held=float(trades["bars_held"].mean()),
            fees_paid_pct=float(trades["fees"].sum() / initial_equity),
            funding_paid_pct=float(-trades["funding"].sum() / initial_equity),
            stop_exits=int((trades["reason"] == "stop").sum()),
        )
    else:
        out.update(profit_factor=float("nan"), win_rate=float("nan"), avg_r=float("nan"),
                   avg_bars_held=float("nan"), fees_paid_pct=0.0, funding_paid_pct=0.0, stop_exits=0)
    return out


def window_returns(equity: pd.Series, window_days: int) -> pd.DataFrame:
    """Non-overlapping consecutive windows of `window_days`; return per window (for the 'majority positive' test)."""
    t0 = equity.index[0]
    bucket = ((equity.index - t0) // pd.Timedelta(days=window_days)).astype(int)
    rows = []
    prev_end = equity.iloc[0]
    for b, g in equity.groupby(bucket):
        end = g.iloc[-1]
        rows.append({"window": int(b), "start": g.index[0], "end": g.index[-1],
                     "ret": float(end / prev_end - 1.0), "n_bars": int(len(g))})
        prev_end = end
    return pd.DataFrame(rows)
