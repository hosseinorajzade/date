import math

import numpy as np
import pandas as pd
import pytest
from scipy import stats as sst

from quantbot.backtest import metrics, stats
from quantbot.backtest.trials import TrialRegistry


def test_expected_max_sharpe_matches_known_normal_order_statistics():
    # E[max of N iid N(0,1)]: ~1.54 (N=10), ~2.51 (N=100), ~3.24 (N=1000)
    for n, ref in [(10, 1.539), (100, 2.508), (1000, 3.241)]:
        assert stats.expected_max_sharpe(n, 1.0) == pytest.approx(ref, abs=0.06)


def test_dsr_reduces_to_psr_for_single_trial_and_falls_with_more_trials():
    r = np.random.default_rng(0).normal(0.001, 0.02, 700)
    one = stats.deflated_sharpe(r, 1, 0.0)
    assert one["dsr"] == pytest.approx(one["psr_vs_zero"])
    v = 0.001
    d = [stats.deflated_sharpe(r, n, v)["dsr"] for n in (2, 10, 100, 1000)]
    assert all(a > b for a, b in zip(d, d[1:]))


def test_psr_matches_closed_form_for_normal_returns():
    sr, n = 0.1, 500
    z = sr * math.sqrt(n - 1) / math.sqrt(1 + 0.5 * sr**2)
    assert stats.psr(sr, 0.0, n, 0.0, 3.0) == pytest.approx(sst.norm.cdf(z))


def test_deflation_rejects_best_of_many_random_strategies():
    """The raison d'etre of DSR: the best of 200 zero-skill strategies looks great but must not pass."""
    rng = np.random.default_rng(1)
    T, N = 730, 200
    R = rng.normal(0, 0.02, (T, N))
    srs = np.array([stats.moments(R[:, j])[0] for j in range(N)])
    best = R[:, srs.argmax()]
    ann = srs.max() * math.sqrt(365)
    assert ann > 1.5  # looks like a great strategy...
    d = stats.deflated_sharpe(best, N, float(np.var(srs, ddof=1)))
    assert d["psr_vs_zero"] > 0.95  # ...and an undeflated test would accept it
    assert d["dsr"] < 0.95  # deflation correctly refuses it


def test_effective_n_tracks_independent_clusters():
    rng = np.random.default_rng(2)
    T = 800
    one_factor = rng.normal(size=(T, 1)) + 0.1 * rng.normal(size=(T, 20))
    indep = rng.normal(size=(T, 20))
    clusters = np.hstack([rng.normal(size=(T, 1)) + 0.15 * rng.normal(size=(T, 10)) for _ in range(4)])  # 4 tight groups of 10
    assert stats.effective_n_trials(one_factor) < 2.0
    assert 17 < stats.effective_n_trials(indep) <= 20
    assert 3.0 < stats.effective_n_trials(clusters) < 6.0


@pytest.mark.slow
def test_dsr_false_positive_rate_is_controlled_under_the_null():
    """Calibration: pick the BEST of N zero-skill strategies; DSR (null variance, N trials) should pass 0.95 rarely."""
    rng = np.random.default_rng(7)
    T, N, reps = 730, 60, 400
    hits = 0
    naive_hits = 0
    for _ in range(reps):
        R = rng.standard_t(4, size=(T, N)) * 0.02
        srs = R.mean(axis=0) / R.std(axis=0, ddof=1)
        best = R[:, srs.argmax()]
        d = stats.deflated_sharpe(best, N, stats.null_sharpe_variance(T))
        hits += d["dsr"] >= 0.95
        naive_hits += d["psr_vs_zero"] >= 0.95
    assert naive_hits / reps > 0.5  # without deflation the winner of 60 coin-flips usually "passes"
    assert hits / reps < 0.10  # with deflation it essentially never does (nominal 5%)


def test_metrics_known_values():
    eq = pd.Series([1.0, 1.1, 0.99, 1.0, 1.2], index=pd.date_range("2024-01-01", periods=5, freq="1D", tz="UTC"))
    assert metrics.max_drawdown(eq.to_numpy()) == pytest.approx(0.1)  # 1.1 -> 0.99
    assert metrics.profit_factor(np.array([3.0, -1.0, 2.0, -1.0])) == pytest.approx(2.5)
    r = np.array([0.01, -0.02, 0.03, 0.0, 0.01])
    assert metrics.sharpe(r) == pytest.approx(r.mean() / r.std(ddof=1) * math.sqrt(365))
    dd = math.sqrt(np.mean(np.minimum(r, 0) ** 2))
    assert metrics.sortino(r) == pytest.approx(r.mean() / dd * math.sqrt(365))


def test_window_returns_partition_and_compound():
    idx = pd.date_range("2024-01-01", periods=24 * 20, freq="1h", tz="UTC")
    eq = pd.Series(np.linspace(1.0, 2.0, len(idx)), index=idx)
    w = metrics.window_returns(eq, 5)
    assert len(w) == 4
    assert (1 + w["ret"]).prod() == pytest.approx(eq.iloc[-1] / eq.iloc[0], rel=1e-9)


def test_trade_sequence_monte_carlo_sane():
    out = stats.trade_sequence_monte_carlo(np.array([0.02, -0.01] * 100), n_paths=2000, seed=0)
    assert out["p_profit"] > 0.95 and out["mdd_p95"] < 0.2
    losing = stats.trade_sequence_monte_carlo(np.array([0.01, -0.02] * 100), n_paths=2000, seed=0)
    assert losing["p_profit"] < 0.05


def test_trial_registry_counts_every_config_and_persists(tmp_path):
    reg = TrialRegistry(tmp_path)
    idx = pd.date_range("2024-01-01", periods=100, freq="1D", tz="UTC")
    rng = np.random.default_rng(0)
    for i in range(5):
        reg.record("fam", {"x": i}, pd.Series(rng.normal(0, 0.01, 100), index=idx))
    reg.record("fam", {"x": 0}, pd.Series(rng.normal(0, 0.01, 100), index=idx))  # re-record same config: not a new trial
    reg.flush()
    again = TrialRegistry(tmp_path)
    assert again.n_trials == 5
    assert again.deflation_inputs()["n_trials_raw"] == 5
