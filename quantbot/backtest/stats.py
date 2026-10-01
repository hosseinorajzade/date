"""Statistical-significance tools: PSR, deflated Sharpe, expected-max-Sharpe, bootstraps.

References: Bailey & Lopez de Prado (2012) "The Sharpe Ratio Efficient Frontier";
            Bailey & Lopez de Prado (2014) "The Deflated Sharpe Ratio";
            Politis & Romano (1994) stationary bootstrap.
All Sharpe ratios here are PER-PERIOD (not annualised) unless the name says otherwise.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import stats as sst

EULER_GAMMA = 0.5772156649015329


def moments(ret: np.ndarray) -> tuple[float, float, float, int]:
    r = np.asarray(ret, dtype=float)
    r = r[~np.isnan(r)]
    n = len(r)
    sr = r.mean() / r.std(ddof=1) if n > 1 and r.std(ddof=1) > 0 else float("nan")
    skew = float(sst.skew(r)) if n > 2 else 0.0
    kurt = float(sst.kurtosis(r, fisher=False)) if n > 3 else 3.0  # raw kurtosis (normal = 3)
    return sr, skew, kurt, n


def psr(sr: float, sr_benchmark: float, n_obs: int, skew: float, kurt: float) -> float:
    """Probabilistic Sharpe Ratio: P(true SR > benchmark) given sample SR, non-normality, sample length."""
    if n_obs < 3 or math.isnan(sr):
        return float("nan")
    denom = 1.0 - skew * sr + (kurt - 1.0) / 4.0 * sr**2
    if denom <= 0:
        return float("nan")
    z = (sr - sr_benchmark) * math.sqrt(n_obs - 1) / math.sqrt(denom)
    return float(sst.norm.cdf(z))


def expected_max_sharpe(n_trials: int, trial_sr_var: float) -> float:
    """E[max of N iid Sharpe estimates] under the null of zero true Sharpe (per-period units)."""
    if n_trials <= 1 or trial_sr_var <= 0:
        return 0.0
    return float(math.sqrt(trial_sr_var) * ((1 - EULER_GAMMA) * sst.norm.ppf(1 - 1.0 / n_trials)
                                            + EULER_GAMMA * sst.norm.ppf(1 - 1.0 / (n_trials * math.e))))


def deflated_sharpe(ret: np.ndarray, n_trials: int, trial_sr_var: float) -> dict:
    """Deflated Sharpe Ratio of a return series given the number of strategy variants tried.

    `trial_sr_var` is the cross-sectional variance of the per-period Sharpe ratios of ALL variants
    tried (not only the winner). Returns PSR vs the expected-max benchmark SR0.
    """
    sr, skew, kurt, n = moments(ret)
    sr0 = expected_max_sharpe(n_trials, trial_sr_var)
    return {"sr_period": sr, "sr0_period": sr0, "n_obs": n, "skew": skew, "kurtosis": kurt,
            "n_trials": n_trials, "dsr": psr(sr, sr0, n, skew, kurt),
            "psr_vs_zero": psr(sr, 0.0, n, skew, kurt)}


def effective_n_trials(trial_returns: np.ndarray) -> float:
    """Effective number of INDEPENDENT trials among N correlated strategy variants.

    Participation ratio of the correlation-matrix spectrum: N_eff = (sum lam)^2 / sum lam^2.
    Independent trials -> N_eff ~ N; perfectly correlated -> 1; k tight clusters -> ~k.
    (The "average correlation" shortcut rho + (1-rho)N badly over-counts when a few families are internally
    near-identical but mutually uncorrelated, so it is not used.)
    """
    x = np.asarray(trial_returns, dtype=float)
    if x.ndim != 2 or x.shape[1] <= 1:
        return float(x.shape[1]) if x.ndim == 2 else 1.0
    keep = x.std(axis=0) > 0
    x = x[:, keep]
    if x.shape[1] <= 1:
        return 1.0
    lam = np.clip(np.linalg.eigvalsh(np.corrcoef(x, rowvar=False)), 0.0, None)
    return float(lam.sum() ** 2 / (lam**2).sum())


def null_sharpe_variance(n_obs: int) -> float:
    """Sampling variance of a per-period Sharpe estimate when the true Sharpe is 0: 1/(T-1) (normal, iid)."""
    return 1.0 / max(n_obs - 1, 1)


def stationary_bootstrap_indices(n: int, mean_block: float, rng: np.random.Generator) -> np.ndarray:
    p = 1.0 / mean_block
    idx = np.empty(n, dtype=np.int64)
    idx[0] = rng.integers(n)
    jumps = rng.random(n) < p
    starts = rng.integers(n, size=n)
    for t in range(1, n):
        idx[t] = starts[t] if jumps[t] else (idx[t - 1] + 1) % n
    return idx


def bootstrap_sharpe_ci(daily_ret: np.ndarray, n_boot: int = 2000, mean_block: float = 10.0, seed: int = 0,
                        ann: float = 365.0) -> dict:
    r = np.asarray(daily_ret, dtype=float)
    r = r[~np.isnan(r)]
    rng = np.random.default_rng(seed)
    out = np.empty(n_boot)
    for b in range(n_boot):
        s = r[stationary_bootstrap_indices(len(r), mean_block, rng)]
        sd = s.std(ddof=1)
        out[b] = s.mean() / sd * math.sqrt(ann) if sd > 0 else np.nan
    return {"sharpe_p05": float(np.nanpercentile(out, 5)), "sharpe_p50": float(np.nanpercentile(out, 50)),
            "sharpe_p95": float(np.nanpercentile(out, 95)), "p_sharpe_gt_0": float(np.nanmean(out > 0))}


def trade_sequence_monte_carlo(trade_returns: np.ndarray, n_paths: int = 5000, seed: int = 0,
                               n_draw: int | None = None) -> dict:
    """Bootstrap the trade sequence (iid resampling of per-trade equity returns) -> terminal return and max-DD distribution."""
    x = np.asarray(trade_returns, dtype=float)
    x = x[~np.isnan(x)]
    if len(x) < 5:
        return {"n_trades": int(len(x)), "note": "too few trades"}
    rng = np.random.default_rng(seed)
    m = n_draw or len(x)
    draws = x[rng.integers(len(x), size=(n_paths, m))]
    eq = np.cumprod(1.0 + draws, axis=1)
    peak = np.maximum.accumulate(np.concatenate([np.ones((n_paths, 1)), eq], axis=1), axis=1)[:, 1:]
    mdd = (1.0 - eq / peak).max(axis=1)
    final = eq[:, -1] - 1.0
    return {"n_trades": int(len(x)), "p_profit": float((final > 0).mean()),
            "final_return_p05": float(np.percentile(final, 5)), "final_return_p50": float(np.percentile(final, 50)),
            "final_return_p95": float(np.percentile(final, 95)),
            "mdd_p50": float(np.percentile(mdd, 50)), "mdd_p95": float(np.percentile(mdd, 95)),
            "mdd_p99": float(np.percentile(mdd, 99)), "p_mdd_gt_20": float((mdd > 0.20).mean())}
