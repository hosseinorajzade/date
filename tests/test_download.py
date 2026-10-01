import pandas as pd
import pytest

from quantbot.data import download
from quantbot.data.download import fetch_funding, fetch_ohlcv
from quantbot.data.store import load_clean

H = 3_600_000


class FakeExchange:
    """Binance-like paging: returns up to `limit` bars starting at `since`; occasionally raises."""

    def __init__(self, n_bars, now_offset=30 * 60_000, fail_first=0):
        self.t0 = 1_600_000_000_000 // H * H
        self.n = n_bars
        self._now = self.t0 + n_bars * H + now_offset  # current hour is still forming
        self.calls, self.fail_first = 0, fail_first

    def milliseconds(self):
        return self._now

    def fetch_ohlcv(self, symbol, timeframe, since=None, limit=1000):
        self.calls += 1
        if self.calls <= self.fail_first:
            raise ConnectionError("temporary")
        k0 = max(0, (since - self.t0 + H - 1) // H)
        rows = [[self.t0 + k * H, 1.0 + k, 2.0 + k, 0.5 + k, 1.5 + k, 10.0] for k in range(int(k0), min(self.n + 1, int(k0) + limit))]
        return rows  # includes the still-forming bar at index n

    def fetch_funding_rate_history(self, symbol, since=None, limit=1000):
        self.calls += 1
        ts = [self.t0 + k * 8 * H for k in range(5)]
        return [{"timestamp": t, "fundingRate": 0.0001} for t in ts if t >= (since or 0)]


def test_fetch_ohlcv_paginates_dedupes_and_drops_forming_bar(monkeypatch):
    monkeypatch.setattr(download.time, "sleep", lambda s: None)
    ex = FakeExchange(2500, fail_first=2)
    df = fetch_ohlcv(ex, "BTC/USDT:USDT", "1h", ex.t0, limit=1000)
    assert len(df) == 2500  # the 2501st (forming) bar is excluded
    assert df.index.is_monotonic_increasing and not df.index.duplicated().any()
    assert (df.index[1:] - df.index[:-1] == pd.Timedelta(hours=1)).all()
    assert df.index.tz is not None and ex.calls >= 5  # 2 failures retried + 3 pages


def test_fetch_ohlcv_gives_up_after_retries(monkeypatch):
    monkeypatch.setattr(download.time, "sleep", lambda s: None)
    ex = FakeExchange(10, fail_first=100)
    with pytest.raises(RuntimeError):
        fetch_ohlcv(ex, "X", "1h", ex.t0)


def test_fetch_funding_and_load_clean_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(download.time, "sleep", lambda s: None)
    ex = FakeExchange(300)
    f = fetch_funding(ex, "BTC/USDT:USDT", ex.t0)
    assert len(f) == 5 and f["rate"].iloc[0] == 0.0001
    cfg = {"market": {"exchange": "binanceusdm", "primary": "BTC/USDT:USDT", "timeframe": "1h", "start": "2020-09-13",
                      "end": None, "data_dir": str(tmp_path), "universe": ["BTC/USDT:USDT"]}}
    (tmp_path / "raw").mkdir()
    df = fetch_ohlcv(ex, "BTC/USDT:USDT", "1h", ex.t0)
    df.to_parquet(download.raw_path(download.Paths(tmp_path), "binanceusdm", "BTC/USDT:USDT", "1h"))
    clean, rep = load_clean(cfg)
    assert len(clean) == 300 and rep.n_gaps == 0 and clean["valid"].all()
    with pytest.raises(FileNotFoundError, match="quantbot.data.download"):
        load_clean(cfg, "ETH/USDT:USDT")
