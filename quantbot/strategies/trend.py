"""Family A — Donchian channel trend following (time-series momentum).

Hypothesis: crypto returns exhibit positive serial dependence at multi-day horizons (slow information
diffusion, herding, leverage-driven feedback). A price breaking out of its N-bar range signals a
regime of persistent drift. Edge is expected to be small per trade, positively skewed (few large
winners), and to cost-drag heavily on a 1h grid, so the lookbacks are long (1-8 days).
Exit: close below the lowest low of the previous N/2 bars (symmetrical for shorts) or ATR stop.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from numba import njit

from .base import Strategy
from .features import atr


@njit(cache=True)
def _donchian_state(close, hh, ll, xl, xs, allow_short):
    n = len(close)
    out = np.zeros(n)
    pos = 0.0
    for i in range(n):
        if np.isnan(hh[i]) or np.isnan(ll[i]) or np.isnan(close[i]):
            pos = 0.0
            out[i] = 0.0
            continue
        if pos == 0.0:
            if close[i] > hh[i]:
                pos = 1.0
            elif allow_short and close[i] < ll[i]:
                pos = -1.0
        elif pos > 0.0:
            if close[i] < xl[i]:
                pos = 0.0
                if allow_short and close[i] < ll[i]:
                    pos = -1.0
        else:
            if close[i] > xs[i]:
                pos = 0.0
                if close[i] > hh[i]:
                    pos = 1.0
        out[i] = pos
    return out


class DonchianTrend(Strategy):
    name = "donchian"
    param_grid = {"n": [24, 48, 96, 192], "k_atr": [2.0, 3.0, 4.0], "allow_short": [False, True]}
    description = "Donchian breakout trend-following with ATR stop"
    rationale = "time-series momentum / slow information diffusion"

    def _raw(self, df):
        n, k, short = self.params["n"], self.params["k_atr"], self.params["allow_short"]
        m = max(n // 2, 2)
        hh = df["high"].rolling(n).max().shift(1)
        ll = df["low"].rolling(n).min().shift(1)
        xl = df["low"].rolling(m).min().shift(1)
        xs = df["high"].rolling(m).max().shift(1)
        state = _donchian_state(df["close"].to_numpy(), hh.to_numpy(), ll.to_numpy(), xl.to_numpy(),
                                xs.to_numpy(), bool(short))
        return pd.Series(state, index=df.index), k * atr(df, 14)

    def warmup_bars(self):
        return self.params["n"] + 14
