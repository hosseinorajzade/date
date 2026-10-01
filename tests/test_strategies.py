import numpy as np
import pandas as pd
import pytest

from quantbot.data.synthetic import null_market
from quantbot.strategies import FAMILIES, make
from quantbot.strategies.audit import check_no_lookahead
from quantbot.strategies.base import Strategy
from quantbot.strategies.ml import walk_forward_proba
from .conftest import make_bars


@pytest.fixture(scope="module")
def mkt():
    return null_market(seed=11, n_bars=24 * 365)


# ---- the audit must be able to CATCH leakage (otherwise passing it means nothing) ---------------
class LeakyShift(Strategy):
    name = "leaky_shift"
    param_grid = {"x": [1]}

    def _raw(self, df):  # peeks at the next bar's return
        return np.sign(df["close"].shift(-1) - df["close"]), df["close"] * 0.02


class LeakyFullSampleZ(Strategy):
    name = "leaky_fullsample"
    param_grid = {"x": [1]}

    def _raw(self, df):  # normalises with whole-sample statistics (future information)
        z = (df["close"] - df["close"].mean()) / df["close"].std()
        return pd.Series(np.where(z < -0.5, 1.0, np.where(z > 0.5, -1.0, 0.0)), index=df.index), df["close"] * 0.02


class LeakyCentered(Strategy):
    name = "leaky_centered"
    param_grid = {"x": [1]}

    def _raw(self, df):  # centred rolling window sees `n/2` future bars
        m = df["close"].rolling(25, center=True).mean()
        return np.sign(df["close"] - m), df["close"] * 0.02


@pytest.mark.parametrize("cls", [LeakyShift, LeakyFullSampleZ, LeakyCentered])
def test_audit_detects_known_leaks(cls, mkt):
    assert check_no_lookahead(cls(x=1), mkt, n_cuts=8), f"{cls.__name__} leak was not detected"


# ---- every shipped family must pass ------------------------------------------------------------
@pytest.mark.parametrize("name", ["donchian", "meanrev", "squeeze"])
def test_rule_families_have_no_lookahead(name, mkt):
    cls = FAMILIES[name]
    cfgs = cls.configs()
    for p in (cfgs[0], cfgs[len(cfgs) // 2], cfgs[-1]):
        assert check_no_lookahead(make(name, **p), mkt, n_cuts=6) == [], p


@pytest.mark.slow
def test_ml_family_has_no_lookahead():
    df = null_market(seed=5, n_bars=24 * 300)
    s = make("ml_gbm", horizon=6, delta=0.03, k_atr=3.0)
    assert check_no_lookahead(s, df, cut_points=[24 * 200, 24 * 250, 24 * 299], n_cuts=3) == []


@pytest.mark.slow
def test_ml_scores_ignore_future_prices():
    df = null_market(seed=6, n_bars=24 * 260)
    k = 24 * 220
    p_full = walk_forward_proba(df, horizon=24)
    df2 = df.copy()
    df2.iloc[k + 1:, :4] = df2.iloc[k + 1:, :4].to_numpy()[::-1] * 2.0
    df2.iloc[k + 1:, 4] = 5.0
    p_alt = walk_forward_proba(df2, horizon=24)
    assert np.allclose(p_full[: k + 1], p_alt[: k + 1], equal_nan=True)
    assert np.isnan(p_full[: 24 * 180 - 1]).all()  # nothing is scored before the first model exists


def test_signals_zero_on_invalid_bars_and_stops_positive(mkt):
    df = mkt.copy()
    df.loc[df.index[3000:3100], ["open", "high", "low", "close"]] = np.nan
    df["valid"] = df["close"].notna()
    for name in ("donchian", "meanrev", "squeeze"):
        sig = make(name, **FAMILIES[name].configs()[0]).generate(df)
        assert (sig.loc[~df["valid"], "target"] == 0).all()
        active = sig["target"] != 0
        assert (sig.loc[active, "stop_dist"] > 0).all()


def test_donchian_goes_long_in_uptrend_and_respects_allow_short():
    n = 400
    up = make_bars(np.linspace(100, 200, n) + np.sin(np.arange(n)))
    long_only = make("donchian", n=24, k_atr=3.0, allow_short=False).generate(up)
    assert (long_only["target"] > 0).sum() > 100 and (long_only["target"] < 0).sum() == 0
    down = make_bars(np.linspace(200, 100, n) + np.sin(np.arange(n)))
    assert (make("donchian", n=24, k_atr=3.0, allow_short=False).generate(down)["target"] <= 0).all()
    assert (make("donchian", n=24, k_atr=3.0, allow_short=True).generate(down)["target"] < 0).sum() > 100


def test_meanrev_fades_a_spike_and_exits_at_mean():
    rng = np.random.default_rng(0)
    c = 100 + rng.normal(0, 0.3, 400).cumsum() * 0.0 + rng.normal(0, 0.3, 400)  # noisy flat series
    c[300] = 110.0  # spike far above the mean
    df = make_bars(c)
    sig = make("meanrev", lookback=48, z_in=2.0, k_atr=3.0, er_max=1.01).generate(df)
    assert sig["target"].iloc[300] == -1.0  # fade the spike
    assert sig["target"].iloc[320] == 0.0  # reverted to the mean -> flat
