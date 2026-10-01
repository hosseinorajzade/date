"""Family C — volatility-compression breakout.

Hypothesis: volatility is clustered and mean-reverting; a period of unusually low Bollinger bandwidth
(compression) is followed by expansion, and the direction of the first close outside the band
carries information about the direction of the expansion (stop-run / breakout participation).
Exit: close back through the mid-band, or a trailing ATR stop (engine-level trailing).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from numba import njit

from .base import Strategy
from .features import atr


@njit(cache=True)
def _squeeze_state(close, mid, up_prev, lo_prev, recent_sq):
    n = len(close)
    out = np.zeros(n)
    pos = 0.0
    for i in range(n):
        if np.isnan(mid[i]) or np.isnan(up_prev[i]) or np.isnan(close[i]):
            pos = 0.0
            continue
        if pos == 0.0:
            if recent_sq[i] > 0.5:
                if close[i] > up_prev[i]:
                    pos = 1.0
                elif close[i] < lo_prev[i]:
                    pos = -1.0
        elif pos > 0.0:
            if close[i] < mid[i]:
                pos = 0.0
        else:
            if close[i] > mid[i]:
                pos = 0.0
        out[i] = pos
    return out


class SqueezeBreakout(Strategy):
    name = "squeeze"
    trail = True
    param_grid = {"lookback": [24, 48], "quantile": [0.10, 0.20], "k_atr": [2.0, 3.0, 4.0]}
    description = "Bollinger-bandwidth squeeze breakout with trailing ATR stop"
    rationale = "volatility clustering: compression precedes expansion"
    WINDOW = 480  # bars used to rank current bandwidth (20 days)
    SQUEEZE_MEMORY = 12  # a squeeze counts if it occurred within the previous 12 bars

    def _raw(self, df):
        L, q, k = self.params["lookback"], self.params["quantile"], self.params["k_atr"]
        c = df["close"]
        mid = c.rolling(L).mean()
        sd = c.rolling(L).std()
        bw = 4.0 * sd / mid
        thr = bw.rolling(self.WINDOW).quantile(q)
        squeeze = (bw <= thr).astype(float)
        recent = squeeze.rolling(self.SQUEEZE_MEMORY).max().shift(1).fillna(0.0)  # squeeze strictly before bar t
        up_prev = (mid + 2 * sd).shift(1)
        lo_prev = (mid - 2 * sd).shift(1)
        state = _squeeze_state(c.to_numpy(), mid.to_numpy(), up_prev.to_numpy(), lo_prev.to_numpy(), recent.to_numpy())
        return pd.Series(state, index=df.index), k * atr(df, 14)

    def warmup_bars(self):
        return self.WINDOW + self.params["lookback"]
