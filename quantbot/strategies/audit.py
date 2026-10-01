"""Look-ahead audit: truncation invariance.

If a signal at bar t depends only on bars <= t, then recomputing the strategy on df.iloc[:t+1] must
reproduce exactly the same decision at t as computing on the full history. Any dependence on future
bars (shift(-k), centred windows, full-sample normalisation, ...) breaks this equality.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Strategy


def check_no_lookahead(strategy: Strategy, df: pd.DataFrame, cut_points: list[int] | None = None,
                       n_cuts: int = 6, seed: int = 0, atol: float = 1e-9) -> list[dict]:
    """Return a list of violations (empty list == audit passed)."""
    full = strategy.generate(df)
    rng = np.random.default_rng(seed)
    lo = min(strategy.warmup_bars() + 50, len(df) - 2)
    cuts = cut_points or sorted(rng.integers(lo, len(df) - 1, size=n_cuts).tolist())
    bad = []
    for k in cuts:
        part = strategy.generate(df.iloc[: k + 1])
        a, b = full.iloc[k], part.iloc[k]
        t_ok = np.isclose(a["target"], b["target"], atol=atol, equal_nan=True)
        s_ok = np.isclose(a["stop_dist"], b["stop_dist"], atol=atol, rtol=1e-9, equal_nan=True)
        if not (t_ok and s_ok):
            bad.append({"bar": int(k), "time": str(df.index[k]), "full": a.to_dict(), "truncated": b.to_dict()})
        # the whole prefix must also be identical, not only the last row
        pf = full.iloc[: k + 1]
        if not np.allclose(pf["target"].to_numpy(), part["target"].to_numpy(), atol=atol, equal_nan=True):
            first = int(np.argmax(~np.isclose(pf["target"].to_numpy(), part["target"].to_numpy(), atol=atol,
                                              equal_nan=True)))
            bad.append({"bar": first, "time": str(df.index[first]), "note": "prefix mismatch"})
    return bad
