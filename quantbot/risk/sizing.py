"""Position sizing — a single numba-compiled function shared by backtest, paper and live code.

Fixed-fractional risk: units = (equity * risk_per_trade * conviction) / stop_distance, then capped
so gross notional <= max_leverage * equity. Because stop distance is k*ATR this is also an
approximate volatility target: size shrinks automatically when volatility rises.
"""
from __future__ import annotations

import math

from numba import njit


@njit(cache=True)
def position_size(equity: float, price: float, stop_dist: float, conviction: float,
                  risk_per_trade: float, max_leverage: float, min_stop_pct: float) -> float:
    """Return unsigned position size in base units (0.0 if inputs are invalid)."""
    if not (equity > 0.0 and price > 0.0) or math.isnan(stop_dist) or math.isnan(conviction):
        return 0.0
    sd = max(stop_dist, min_stop_pct * price)
    if sd <= 0.0:
        return 0.0
    conv = min(max(conviction, 0.0), 1.0)
    units = equity * risk_per_trade * conv / sd
    cap = max_leverage * equity / price
    return min(units, cap)
