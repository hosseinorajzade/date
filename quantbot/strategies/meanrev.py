"""Family B — short-horizon mean reversion in choppy regimes.

Hypothesis: on hourly horizons, large deviations from a rolling mean in NON-trending conditions
(low Kaufman efficiency ratio) are dominated by liquidity shocks (forced liquidations, thin books)
that partly revert; liquidity providers are paid to absorb them. Not expected to work when a genuine
trend is underway, hence the efficiency-ratio gate. Exit at the mean, after 2L bars, or ATR stop.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from numba import njit

from .base import Strategy
from .features import atr, efficiency_ratio


@njit(cache=True)
def _meanrev_state(z, gate_ok, zin, max_hold):
    n = len(z)
    out = np.zeros(n)
    pos = 0.0
    held = 0
    for i in range(n):
        if np.isnan(z[i]):
            pos = 0.0
            held = 0
            continue
        if pos == 0.0:
            if gate_ok[i] and z[i] < -zin:
                pos, held = 1.0, 0
            elif gate_ok[i] and z[i] > zin:
                pos, held = -1.0, 0
        else:
            held += 1
            if (pos > 0 and z[i] >= 0.0) or (pos < 0 and z[i] <= 0.0) or held >= max_hold:
                pos = 0.0
        out[i] = pos
    return out


class ZScoreMeanReversion(Strategy):
    name = "meanrev"
    param_grid = {"lookback": [24, 48, 96], "z_in": [2.0, 2.5, 3.0], "k_atr": [2.0, 3.0], "er_max": [0.35, 1.01]}
    description = "Z-score mean reversion gated by low efficiency ratio"
    rationale = "liquidity-driven overreaction reverts in non-trending regimes"

    def _raw(self, df):
        L, zin, k, er_max = (self.params[x] for x in ("lookback", "z_in", "k_atr", "er_max"))
        c = df["close"]
        z = (c - c.rolling(L).mean()) / c.rolling(L).std().replace(0, np.nan)
        er = efficiency_ratio(c, L)
        gate = (er < er_max).fillna(False).to_numpy()
        state = _meanrev_state(z.to_numpy(), gate, float(zin), int(2 * L))
        return pd.Series(state, index=df.index), k * atr(df, 14)

    def warmup_bars(self):
        return self.params["lookback"] + 14
