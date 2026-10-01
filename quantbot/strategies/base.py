"""Strategy interface.

A strategy turns OHLCV history into a per-bar decision STATE:
    target[t]    in [-1, 1]  desired direction/conviction, decided at the CLOSE of bar t
    stop_dist[t] > 0         stop distance in price units for a position opened on that decision
Row t may only depend on rows <= t (enforced by strategies.audit + tests). The engine executes the
decision at the open of bar t+1.
"""
from __future__ import annotations

import itertools
from abc import ABC, abstractmethod
from typing import Any

import numpy as np
import pandas as pd


class Strategy(ABC):
    name: str = "base"
    trail: bool = False  # engine-level trailing stop
    param_grid: dict[str, list] = {}
    description: str = ""
    rationale: str = ""

    def __init__(self, **params: Any):
        unknown = set(params) - set(self.param_grid)
        if unknown:
            raise ValueError(f"{self.name}: unknown params {unknown}")
        missing = set(self.param_grid) - set(params)
        if missing:
            raise ValueError(f"{self.name}: missing params {missing}")
        self.params = dict(params)

    # -- to be implemented -------------------------------------------------------------------
    @abstractmethod
    def _raw(self, df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
        """Return (target, stop_dist) aligned to df.index; NaN allowed during warm-up."""

    # -- public ------------------------------------------------------------------------------
    def generate(self, df: pd.DataFrame) -> pd.DataFrame:
        target, stop = self._raw(df)
        target = target.reindex(df.index).astype(float)
        stop = stop.reindex(df.index).astype(float)
        bad = target.isna() | stop.isna() | ~(stop > 0)
        if "valid" in df.columns:
            bad |= ~df["valid"].astype(bool)
        target = target.where(~bad, 0.0)
        stop = stop.where(~bad, np.nan)
        return pd.DataFrame({"target": target, "stop_dist": stop}, index=df.index)

    @classmethod
    def configs(cls) -> list[dict]:
        keys = list(cls.param_grid)
        return [dict(zip(keys, vals)) for vals in itertools.product(*(cls.param_grid[k] for k in keys))]

    @classmethod
    def neighbors(cls, params: dict) -> list[dict]:
        """Configs that differ from `params` by one grid step in exactly one parameter."""
        out = []
        for k, grid in cls.param_grid.items():
            i = grid.index(params[k])
            for j in (i - 1, i + 1):
                if 0 <= j < len(grid):
                    out.append({**params, k: grid[j]})
        return out

    def warmup_bars(self) -> int:
        return 0

    def __repr__(self) -> str:
        return f"{self.name}({', '.join(f'{k}={v}' for k, v in self.params.items())})"
