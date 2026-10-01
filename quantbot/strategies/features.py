"""Causal feature helpers. Every function uses only data up to and including bar t at row t."""
from __future__ import annotations

import numpy as np
import pandas as pd


def true_range(df: pd.DataFrame) -> pd.Series:
    pc = df["close"].shift(1)
    return pd.concat([df["high"] - df["low"], (df["high"] - pc).abs(), (df["low"] - pc).abs()], axis=1).max(axis=1)


def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    """Wilder ATR (EWM alpha=1/n). Row t uses bars <= t."""
    return true_range(df).ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()


def log_ret(close: pd.Series, n: int = 1) -> pd.Series:
    return np.log(close).diff(n)


def realized_vol(close: pd.Series, n: int) -> pd.Series:
    return log_ret(close, 1).rolling(n).std()


def efficiency_ratio(close: pd.Series, n: int) -> pd.Series:
    """Kaufman efficiency ratio: |net move| / sum |moves| over n bars. ~1 trending, ~0 choppy."""
    net = (close - close.shift(n)).abs()
    path = close.diff().abs().rolling(n).sum()
    return net / path.replace(0, np.nan)


def rsi(close: pd.Series, n: int = 14) -> pd.Series:
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))


def zscore(s: pd.Series, n: int) -> pd.Series:
    return (s - s.rolling(n).mean()) / s.rolling(n).std().replace(0, np.nan)
