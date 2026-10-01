"""Synthetic OHLCV generators — FOR FRAMEWORK VALIDATION ONLY.

Nothing produced here may be reported as evidence of a trading edge. They exist to answer two
questions about the *pipeline*:
  (a) null market  -> does the pipeline (walk-forward, hold-out, DSR) correctly reject?
  (b) planted edge -> does it have the power to detect a known, genuine edge?

Null-market model (an exact MARTINGALE in the trader's information set, at every intrabar step):
  * each bar is built from `substeps` (default 120) iid-Gaussian log-increments whose variance is
        v_t = sigma_t^2 * w_t,   sigma_t : GARCH(1,1) clustering x intraday seasonality
                                 w_t     : inverse-chi-square mixing => Student-t(df) bar returns (fat tails)
  * every increment carries a -variance/2 convexity correction, so E[P_{k+1}/P_k | past] = 1 exactly
    (zero ARITHMETIC drift; a zero *log* drift would hand long positions a +sigma^2/2 free lunch);
  * no endpoint-conditioned bridges: intrabar paths are real random walks, so high/low excursions are
    realistic and stop orders cannot profit from intrabar structure (this bug existed in v1: see journal).
Planted-trend market: adds an Ornstein-Uhlenbeck drift mu_t with a multi-day half-life (harvestable by trend followers).
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def make_market(n_bars: int = 24 * 365 * 7, seed: int = 0, start: str = "2019-10-01",
                annual_vol: float = 0.70, drift_ann: float = 0.0, df_t: float = 4.0,
                trend_strength: float = 0.0, trend_halflife_hours: float = 24 * 6,
                substeps: int = 120, start_price: float = 8000.0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n = n_bars
    base_sigma = annual_vol / np.sqrt(24 * 365)  # hourly
    alpha, beta = 0.07, 0.91  # GARCH(1,1); stationary variance == base_sigma^2
    hour = np.arange(n) % 24
    seasonal = 1 + 0.25 * np.sin(2 * np.pi * (hour - 8) / 24)

    # inverse-chi-square mixing => Student-t bar returns with unit mean variance
    w = (df_t - 2.0) / rng.chisquare(df_t, size=n)
    z = rng.standard_normal((n, substeps))

    mu = np.zeros(n)  # persistent drift (OU), std = trend_strength * base_sigma per hour
    if trend_strength > 0:
        phi = np.exp(-np.log(2) / trend_halflife_hours)
        innov = rng.standard_normal(n) * np.sqrt(1 - phi**2)
        zz = np.zeros(n)
        for i in range(1, n):
            zz[i] = phi * zz[i - 1] + innov[i]
        mu = trend_strength * base_sigma * zz
    mu = mu + drift_ann / (24 * 365)

    log_close = np.empty(n)
    log_open = np.empty(n)
    path_hi = np.empty(n)
    path_lo = np.empty(n)
    h = base_sigma**2
    last_r = 0.0
    x = np.log(start_price)
    for i in range(n):
        h = base_sigma**2 * (1 - alpha - beta) + alpha * last_r**2 + beta * h
        v = h * seasonal[i] ** 2 * w[i]  # bar variance
        vs = v / substeps
        inc = mu[i] / substeps - vs / 2.0 + np.sqrt(vs) * z[i]  # martingale-corrected log increments
        path = x + np.cumsum(inc)
        log_open[i] = x
        path_hi[i], path_lo[i] = path.max(), path.min()
        x = path[-1]
        log_close[i] = x
        last_r = (log_close[i] - log_open[i]) + v / 2.0  # innovation (convexity term removed) feeds the GARCH recursion

    o, c = np.exp(log_open), np.exp(log_close)
    hi = np.exp(np.maximum(path_hi, np.maximum(log_open, log_close)))
    lo = np.exp(np.minimum(path_lo, np.minimum(log_open, log_close)))
    r_abs = np.abs(log_close - log_open)
    vol = 1000 * np.exp(0.3 * r_abs / base_sigma + 0.3 * rng.standard_normal(n)) * seasonal
    idx = pd.date_range(start, periods=n, freq="1h", tz="UTC", name="ts")
    df = pd.DataFrame({"open": o, "high": hi, "low": lo, "close": c, "volume": vol}, index=idx)
    df["filled"] = False
    df["valid"] = True
    return df


def null_market(seed: int = 0, **kw) -> pd.DataFrame:
    """Efficient market: price is a martingale. Any 'edge' found here is selection bias or a bug."""
    return make_market(seed=seed, trend_strength=0.0, **kw)


def trending_market(seed: int = 0, trend_strength: float = 0.06, **kw) -> pd.DataFrame:
    """Planted edge: persistent OU drift. Theoretical capture is limited by costs and noise."""
    return make_market(seed=seed, trend_strength=trend_strength, **kw)
