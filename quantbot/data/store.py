"""Load cached, cleaned data. Cleaning is applied on read so raw files stay untouched."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from ..config import Paths
from .clean import clean_ohlcv, CleanReport
from .download import raw_path


def load_clean(cfg: dict, symbol: str | None = None) -> tuple[pd.DataFrame, CleanReport]:
    m = cfg["market"]
    symbol = symbol or m["primary"]
    paths = Paths(Path(m["data_dir"]))
    p = raw_path(paths, m["exchange"], symbol, m["timeframe"])
    if not p.exists():
        raise FileNotFoundError(
            f"{p} not found. Run `python -m quantbot.data.download` (needs exchange API access)."
        )
    raw = pd.read_parquet(p)
    return clean_ohlcv(raw, m["timeframe"])


def load_funding(cfg: dict, symbol: str | None = None) -> pd.Series | None:
    m = cfg["market"]
    symbol = symbol or m["primary"]
    p = raw_path(Paths(Path(m["data_dir"])), m["exchange"], symbol, m["timeframe"], kind="funding")
    if not p.exists():
        return None
    return pd.read_parquet(p)["rate"]


def funding_per_bar(funding: pd.Series | None, index: pd.DatetimeIndex, timeframe_minutes: int,
                    fallback_bps_per_8h: float) -> pd.Series:
    """Per-bar funding rate (fraction of notional; positive = longs pay).

    Real history is spread uniformly over the bars of each 8h interval (the exchange charges at
    00/08/16 UTC; uniform accrual is an approximation that preserves the total cost). Bars before
    the first record use the constant fallback.
    """
    bars_per_8h = 480.0 / timeframe_minutes
    const = fallback_bps_per_8h * 1e-4 / bars_per_8h
    if funding is None or funding.empty:
        return pd.Series(const, index=index)
    # each record applies to the 8h *preceding* its timestamp
    per_bar = (funding / bars_per_8h).reindex(index, method="bfill", limit=int(bars_per_8h))
    return per_bar.fillna(const)
