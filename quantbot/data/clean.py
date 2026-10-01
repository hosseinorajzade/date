"""OHLCV cleaning: UTC index, dedupe, regular grid, gap handling, bad-tick detection.

Design rules
- Never silently invent price information. Short gaps (<= max_fill bars) are filled with a
  flat bar (O=H=L=C=previous close, volume 0) and flagged; longer gaps stay NaN and are
  flagged `valid=False` so strategies emit no signal and the engine does not trade them.
- Real crashes must NOT be removed. A bar is a bad tick only if it spikes and reverts within
  one bar (|r_t| large and r_t + r_{t+1} ~ 0); genuine crashes persist.
- Crypto has no splits/dividends. Equity adjustments would be applied on ingestion (not needed here).
- Survivorship: only assets that existed over the full test window are in the universe; delisted
  coins are absent from any exchange API, so cross-asset results are optimistic by construction.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from ..config import timeframe_to_minutes


@dataclass
class CleanReport:
    n_raw: int = 0
    n_duplicates: int = 0
    n_invalid_rows: int = 0
    n_bad_ticks: int = 0
    n_gap_bars_filled: int = 0
    n_gap_bars_unfilled: int = 0
    n_gaps: int = 0
    longest_gap_bars: int = 0
    first: str = ""
    last: str = ""
    notes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return self.__dict__.copy()


def clean_ohlcv(df: pd.DataFrame, timeframe: str, max_fill: int = 3, spike_sigma: float = 10.0,
                spike_revert: float = 0.35) -> tuple[pd.DataFrame, CleanReport]:
    rep = CleanReport(n_raw=len(df))
    if df.empty:
        return df.copy(), rep
    df = df.copy()
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("index must be a DatetimeIndex")
    df.index = df.index.tz_localize("UTC") if df.index.tz is None else df.index.tz_convert("UTC")
    df = df.sort_index()
    rep.n_duplicates = int(df.index.duplicated().sum())
    df = df[~df.index.duplicated(keep="last")]
    cols = ["open", "high", "low", "close", "volume"]
    df = df[cols].astype(float)

    # 1) structurally invalid rows -> NaN (dropped by the regular-grid reindex)
    bad = (
        (df[["open", "high", "low", "close"]] <= 0).any(axis=1)
        | df[["open", "high", "low", "close"]].isna().any(axis=1)
        | (df["high"] < df["low"])
        | (df["volume"] < 0)
    )
    # tolerate tiny rounding: close/open outside [low, high] by > 0.1% is bad, otherwise clip
    tol = 1e-3
    out = (
        (df["close"] > df["high"] * (1 + tol)) | (df["close"] < df["low"] * (1 - tol))
        | (df["open"] > df["high"] * (1 + tol)) | (df["open"] < df["low"] * (1 - tol))
    )
    bad |= out
    rep.n_invalid_rows = int(bad.sum())
    df = df[~bad]
    df["high"] = df[["open", "high", "low", "close"]].max(axis=1)
    df["low"] = df[["open", "high", "low", "close"]].min(axis=1)

    # 2) spike-and-revert bad ticks
    r = np.log(df["close"]).diff()
    scale = r.abs().rolling(500, min_periods=50).median() * 1.4826 + 1e-12
    scale = scale.shift(1)  # only past data defines "normal" so cleaning cannot hide a live-observable move
    spike = (r.abs() > spike_sigma * scale) & ((r + r.shift(-1)).abs() < spike_revert * r.abs())
    rep.n_bad_ticks = int(spike.sum())
    df = df[~spike.fillna(False)]

    # 3) regular grid + gaps
    step = pd.Timedelta(minutes=timeframe_to_minutes(timeframe))
    full = pd.date_range(df.index[0], df.index[-1], freq=step, tz="UTC")
    df = df.reindex(full)
    df.index.name = "ts"
    missing = df["close"].isna()
    if missing.any():
        grp = (missing != missing.shift()).cumsum()
        runs = missing.groupby(grp).agg(["first", "size"])
        gap_runs = runs[runs["first"]]["size"]
        rep.n_gaps = int(len(gap_runs))
        rep.longest_gap_bars = int(gap_runs.max())
        run_len = missing.groupby(grp).transform("size")
        fillable = missing & (run_len <= max_fill)
        prev_close = df["close"].ffill()
        for c in ("open", "high", "low", "close"):
            df.loc[fillable, c] = prev_close[fillable]
        df.loc[fillable, "volume"] = 0.0
        rep.n_gap_bars_filled = int(fillable.sum())
        rep.n_gap_bars_unfilled = int((missing & ~fillable).sum())
    df["filled"] = missing & df["close"].notna()
    df["valid"] = df["close"].notna()
    rep.first, rep.last = str(df.index[0]), str(df.index[-1])
    return df, rep
