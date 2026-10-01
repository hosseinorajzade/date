from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class BarFeed(ABC):
    @abstractmethod
    def history(self, n_bars: int) -> pd.DataFrame: ...

    @abstractmethod
    def new_bars(self, since: pd.Timestamp | None) -> pd.DataFrame:
        """Closed bars strictly after `since` (all closed bars if None), oldest first."""


class ReplayFeed(BarFeed):
    """Deterministic feed over a DataFrame; `advance(k)` reveals k more bars. Used for tests and replay-parity."""

    def __init__(self, df: pd.DataFrame, start: int = 0):
        self.df, self.cursor = df, start

    def advance(self, k: int = 1) -> None:
        self.cursor = min(self.cursor + k, len(self.df))

    def history(self, n_bars: int) -> pd.DataFrame:
        return self.df.iloc[max(0, self.cursor - n_bars): self.cursor]

    def new_bars(self, since):
        vis = self.df.iloc[: self.cursor]
        return vis if since is None else vis[vis.index > since]


class CcxtFeed(BarFeed):
    def __init__(self, client):
        self.client = client

    def history(self, n_bars: int) -> pd.DataFrame:
        return self.client.fetch_history(n_bars)

    def new_bars(self, since):
        return self.client.fetch_closed_bars(since, 1000)
