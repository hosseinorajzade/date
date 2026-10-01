"""Family D — walk-forward gradient-boosted direction model.

Hypothesis: a small, regularised non-linear model on causal price/volume/seasonality features can
extract weak directional information (vol-conditioned momentum/reversal, time-of-day effects) that
simple rules miss. Prior: weak; the family is included because ML is the most overfit-prone approach and
therefore the best stress test of the multiple-testing machinery.

Leakage control
  * features at t use bars <= t only;
  * label_t = 1[close_{t+H} > close_t] is only used for training rows with t + H <= retrain bar b;
  * the model scores bars in [b, b + R) and is retrained on a rolling window every R bars at fixed
    ABSOLUTE positions, so recomputing on a truncated history yields identical scores (audited).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from numba import njit
from sklearn.ensemble import HistGradientBoostingClassifier

from .base import Strategy
from .features import atr, log_ret, realized_vol, rsi

_CACHE: dict = {}


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    c, v = df["close"], df["volume"]
    f = {}
    for n in (1, 3, 6, 12, 24, 48, 96):
        f[f"ret_{n}"] = log_ret(c, n)
    vol24, vol96 = realized_vol(c, 24), realized_vol(c, 96)
    f["vol_24"], f["vol_96"] = vol24, vol96
    f["vol_ratio"] = vol24 / vol96.replace(0, np.nan)
    f["atr_pct"] = atr(df, 14) / c
    lv = np.log1p(v)
    f["vol_z"] = (lv - lv.rolling(168).mean()) / lv.rolling(168).std().replace(0, np.nan)
    hi, lo = df["high"].rolling(24).max(), df["low"].rolling(24).min()
    f["range_pos_24"] = (c - lo) / (hi - lo).replace(0, np.nan)
    f["rsi_14"] = rsi(c, 14)
    f["mom_norm"] = f["ret_24"] / vol96.replace(0, np.nan)
    hour = df.index.hour.to_numpy()
    dow = df.index.dayofweek.to_numpy()
    f["hour_sin"], f["hour_cos"] = np.sin(2 * np.pi * hour / 24), np.cos(2 * np.pi * hour / 24)
    f["dow_sin"], f["dow_cos"] = np.sin(2 * np.pi * dow / 7), np.cos(2 * np.pi * dow / 7)
    return pd.DataFrame(f, index=df.index).replace([np.inf, -np.inf], np.nan)


def walk_forward_proba(df: pd.DataFrame, horizon: int, retrain_every: int = 720, train_bars: int = 24 * 365 * 2,
                       min_train: int = 24 * 180, seed: int = 0) -> np.ndarray:
    """P(up over `horizon` bars) for each bar, from models trained only on already-realised labels."""
    key = (df.index[0], df.index[-1], len(df), horizon, retrain_every, train_bars, min_train, seed,
           float(df["close"].iloc[-1]))
    if key in _CACHE:
        return _CACHE[key]
    X = build_features(df)
    close = df["close"].to_numpy()
    y = np.full(len(df), np.nan)
    y[: len(df) - horizon] = (close[horizon:] > close[: len(df) - horizon]).astype(float)
    y[np.isnan(close)] = np.nan
    Xv = X.to_numpy()
    ok_row = ~np.isnan(Xv).any(axis=1)
    proba = np.full(len(df), np.nan)
    n = len(df)
    b = min_train
    while b < n:
        hi = b - horizon + 1  # rows t <= b - horizon have a realised label by bar b
        lo = max(0, hi - train_bars)
        rows = np.arange(lo, hi)
        rows = rows[ok_row[rows] & ~np.isnan(y[rows])]
        end = min(b + retrain_every, n)
        if len(rows) >= 500 and len(np.unique(y[rows])) == 2:
            model = HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter=100, min_samples_leaf=300,
                                                   l2_regularization=5.0, random_state=seed, early_stopping=False)
            model.fit(Xv[rows], y[rows])
            idx = np.arange(b, end)
            idx = idx[ok_row[idx]]
            if len(idx):
                proba[idx] = model.predict_proba(Xv[idx])[:, 1]
        b = end
    if len(_CACHE) > 64:
        _CACHE.clear()
    _CACHE[key] = proba
    return proba


@njit(cache=True)
def _prob_state(p, delta, hold, allow_short):
    n = len(p)
    out = np.zeros(n)
    pos = 0.0
    held = 0
    for i in range(n):
        if np.isnan(p[i]):
            pos = 0.0
            held = 0
            continue
        s = 0.0
        if p[i] > 0.5 + delta:
            s = 1.0
        elif p[i] < 0.5 - delta and allow_short:
            s = -1.0
        if pos == 0.0:
            pos = s
            held = 0
        else:
            held += 1
            if held >= hold:
                pos = s
                held = 0
        out[i] = pos
    return out


class GBMDirectional(Strategy):
    name = "ml_gbm"
    param_grid = {"horizon": [6, 24], "delta": [0.03, 0.06], "k_atr": [2.0, 3.0]}
    description = "Walk-forward gradient boosting direction model, min-hold = horizon"
    rationale = "weak, non-linear vol-conditioned predictability (high overfit risk)"

    def _raw(self, df):
        H, delta, k = self.params["horizon"], self.params["delta"], self.params["k_atr"]
        p = walk_forward_proba(df, H)
        state = _prob_state(p, float(delta), int(H), True)
        return pd.Series(state, index=df.index), k * atr(df, 14)

    def warmup_bars(self):
        return 24 * 180
