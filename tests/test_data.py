import numpy as np
import pandas as pd
import pytest

from quantbot.data.clean import clean_ohlcv
from quantbot.data.splits import DataSplit, HoldoutAlreadyUsed, HoldoutVault
from quantbot.data.store import funding_per_bar
from quantbot.data.synthetic import null_market


def raw(n=500, seed=0):
    df = null_market(seed=seed, n_bars=n)[["open", "high", "low", "close", "volume"]]
    return df


def test_clean_dedupes_sorts_and_localises_utc():
    df = raw()
    messy = pd.concat([df, df.iloc[10:15]]).sample(frac=1, random_state=0)
    messy.index = messy.index.tz_localize(None)  # naive timestamps
    out, rep = clean_ohlcv(messy, "1h")
    assert out.index.tz is not None and str(out.index.tz) == "UTC"
    assert out.index.is_monotonic_increasing and not out.index.duplicated().any()
    assert rep.n_duplicates == 5 and len(out) == len(df)


def test_short_gaps_filled_flat_long_gaps_left_invalid():
    df = raw(600)
    df = df.drop(df.index[100:102]).drop(df.index[300:320])
    out, rep = clean_ohlcv(df, "1h", max_fill=3)
    assert rep.n_gap_bars_filled == 2 and rep.n_gap_bars_unfilled == 20 and rep.n_gaps == 2
    filled = out.iloc[100:102]
    assert (filled["volume"] == 0).all() and filled["filled"].all()
    assert (filled["open"] == filled["close"]).all() and (filled["close"] == out["close"].iloc[99]).all()
    assert not out["valid"].iloc[300:320].any() and out["valid"].iloc[:300].all()


def test_bad_tick_removed_but_real_crash_kept():
    df = raw(2000)
    spike = df.copy()
    spike.iloc[1500, spike.columns.get_loc("close")] *= 1.5  # one-bar spike that fully reverts next bar
    spike.iloc[1500, spike.columns.get_loc("high")] = spike.iloc[1500]["close"]
    out, rep = clean_ohlcv(spike, "1h")
    assert rep.n_bad_ticks >= 1
    crash = df.copy()
    crash.iloc[1500:, :4] *= 0.7  # a genuine -30% move that persists
    out2, rep2 = clean_ohlcv(crash, "1h")
    assert rep2.n_bad_ticks == 0 and out2["close"].iloc[-1] == pytest.approx(crash["close"].iloc[-1])


def test_invalid_rows_dropped():
    df = raw(300)
    df.iloc[50, df.columns.get_loc("low")] = df.iloc[50]["high"] * 2  # high < low
    df.iloc[60, df.columns.get_loc("close")] = -1.0
    out, rep = clean_ohlcv(df, "1h", max_fill=0)
    assert rep.n_invalid_rows == 2 and not out["valid"].iloc[50] and not out["valid"].iloc[60]


def test_split_is_chronological_disjoint_and_complete():
    df = null_market(seed=1, n_bars=24 * 365 * 3, start="2020-01-01")
    sp = DataSplit(pd.Timestamp("2021-01-01", tz="UTC"), pd.Timestamp("2021-07-01", tz="UTC"))
    tr, va, ho = sp.train(df), sp.validation(df), sp._holdout(df)
    assert len(tr) + len(va) + len(ho) == len(df)
    assert tr.index.max() < va.index.min() and va.index.max() < ho.index.min()
    assert sp.research(df).index.max() == va.index.max()


def test_holdout_vault_one_look_per_family(tmp_path):
    df = null_market(seed=1, n_bars=24 * 400, start="2020-01-01")
    sp = DataSplit(pd.Timestamp("2020-09-01", tz="UTC"), pd.Timestamp("2020-12-01", tz="UTC"))
    vault = HoldoutVault(sp, tmp_path / "log.json")
    ho = vault.open(df, "famA", {"n": 1})
    assert ho.index.min() >= sp.val_end
    with pytest.raises(HoldoutAlreadyUsed):
        vault.open(df, "famA", {"n": 2})
    vault.open(df, "famB", {"n": 1})  # a different family has its own single look
    assert len(vault.used_by("famA")) == 1


def test_funding_per_bar_fallback_and_history():
    idx = pd.date_range("2024-01-01", periods=48, freq="1h", tz="UTC")
    const = funding_per_bar(None, idx, 60, 1.0)
    assert const.iloc[0] == pytest.approx(1e-4 / 8)
    hist = pd.Series([0.0003], index=[pd.Timestamp("2024-01-01 08:00", tz="UTC")])
    f = funding_per_bar(hist, idx, 60, 1.0)
    assert f.loc["2024-01-01 03:00"] == pytest.approx(0.0003 / 8)  # spread over the preceding 8h
    assert f.loc["2024-01-02 12:00"] == pytest.approx(1e-4 / 8)  # beyond history: fallback


@pytest.mark.slow
def test_null_market_is_a_martingale_with_clustered_vol_and_fat_tails():
    rets, hourly_ac, intra = [], [], []
    for seed in range(12):
        df = null_market(seed=seed, n_bars=24 * 365)
        pr = df["close"].pct_change().dropna()
        rets.append(pr.mean() * 24 * 365)
        lr = np.log(df["close"]).diff().dropna()
        hourly_ac.append(lr.autocorr(1))
    se = np.std(rets, ddof=1) / np.sqrt(len(rets))
    assert abs(np.mean(rets)) < 3.5 * se + 0.05  # zero ARITHMETIC drift (a zero-log-drift series would show +0.25/yr)
    assert abs(np.mean(hourly_ac)) < 0.02
    df = null_market(seed=1, n_bars=24 * 365 * 2)
    lr = np.log(df["close"]).diff().dropna()
    assert lr.kurt() > 3 and lr.abs().autocorr(1) > 0.1  # fat tails + volatility clustering
    assert (df["high"] >= df[["open", "close"]].max(axis=1) - 1e-9).all()
    assert (df["low"] <= df[["open", "close"]].min(axis=1) + 1e-9).all()


def test_planted_trend_market_has_more_serial_dependence_than_null():
    from quantbot.data.synthetic import trending_market

    def ac(f, seeds):
        out = []
        for s in seeds:
            d = f(seed=s, n_bars=24 * 365 * 3)
            out.append(np.log(d["close"]).diff().dropna().resample("1D").sum().autocorr(1))
        return np.mean(out)

    assert ac(lambda **k: trending_market(trend_strength=0.12, **k), range(6)) - ac(null_market, range(6)) > 0.04
