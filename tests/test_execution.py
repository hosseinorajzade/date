import copy
import json
import os

import numpy as np
import pandas as pd
import pytest

from quantbot.backtest.engine import EngineConfig, run_backtest
from quantbot.config import load_config
from quantbot.data.synthetic import null_market, trending_market
from quantbot.execution import exchange as exchange_mod
from quantbot.execution.alerts import Alerter, TelegramAlerter
from quantbot.execution.feed import ReplayFeed
from quantbot.execution.gate import LiveNotAllowed, assert_live_allowed, paper_gate
from quantbot.execution.live import LiveTrader
from quantbot.execution.paper import PaperTrader
from quantbot.execution.state import StateStore, TraderState
from quantbot.strategies import make


@pytest.fixture(scope="module")
def cfg():
    return load_config()


def run_paper(cfg, df, strat, tmp, chunk=1, **kw):
    feed = ReplayFeed(df, 0)
    tr = PaperTrader(cfg, strat, feed, StateStore(tmp), Alerter(), initial_equity=1.0, lookback_bars=len(df) + 10, **kw)
    while feed.cursor < len(df):
        feed.advance(chunk)
        tr.step_new_bars()
    return tr, feed


def test_paper_trader_reproduces_backtest_exactly(cfg, tmp_path):
    """Same compiled kernel + same fill model => replaying history through the paper trader == the backtest."""
    df = trending_market(seed=4, n_bars=24 * 120, start="2024-01-01")
    strat = make("donchian", n=24, k_atr=2.0, allow_short=True)
    tr, _ = run_paper(cfg, df, strat, tmp_path)
    sig = strat.generate(df)
    ecfg = EngineConfig.from_config(cfg, trailing=strat.trail)
    funding = cfg["costs"]["funding_bps_per_8h"] * 1e-4 / 8.0
    bt = run_backtest(df, sig["target"], sig["stop_dist"], ecfg, funding=funding)
    paper_eq = pd.read_csv(tmp_path / "equity.csv")["equity"].to_numpy()
    assert len(paper_eq) == len(df)
    assert np.allclose(paper_eq[:-1], bt.equity.to_numpy()[:-1], rtol=0, atol=1e-10)  # last bar differs: backtest force-closes
    paper_tr = pd.read_csv(tmp_path / "trades.csv")
    bt_tr = bt.trades[bt.trades["reason"] != "end_of_data"]
    assert len(paper_tr) == len(bt_tr) > 3
    assert np.allclose(paper_tr["net"].to_numpy(), bt_tr["net"].to_numpy(), atol=1e-10)
    assert (paper_tr["reason"].to_numpy() == bt_tr["reason"].to_numpy()).all()
    assert tr.state.unreconciled_errors == 0 and not tr.state.halted


def test_restart_resumes_and_matches_uninterrupted_run(cfg, tmp_path):
    df = trending_market(seed=5, n_bars=24 * 60, start="2024-01-01")
    strat = make("donchian", n=24, k_atr=3.0, allow_short=True)
    ref, _ = run_paper(cfg, df, strat, tmp_path / "ref")
    feed = ReplayFeed(df, 0)
    store = StateStore(tmp_path / "rs")
    t1 = PaperTrader(cfg, strat, feed, store, Alerter(), initial_equity=1.0, lookback_bars=len(df) + 10)
    feed.advance(500)
    t1.step_new_bars()
    del t1  # "crash"
    t2 = PaperTrader(cfg, strat, feed, StateStore(tmp_path / "rs"), Alerter(), initial_equity=1.0, lookback_bars=len(df) + 10)
    assert t2.state.bars_processed == 500
    feed.advance(len(df))
    t2.step_new_bars()
    a = pd.read_csv(tmp_path / "ref" / "equity.csv")["equity"].to_numpy()
    b = pd.read_csv(tmp_path / "rs" / "equity.csv")["equity"].to_numpy()
    assert np.allclose(a, b, atol=1e-10) and len(a) == len(b) == len(df)


def test_redelivered_bars_are_ignored(cfg, tmp_path):
    df = null_market(seed=1, n_bars=300, start="2024-01-01")
    strat = make("donchian", n=24, k_atr=3.0, allow_short=True)
    feed = ReplayFeed(df, 0)
    tr = PaperTrader(cfg, strat, feed, StateStore(tmp_path), Alerter(), initial_equity=1.0, lookback_bars=400)
    feed.advance(200)
    assert tr.step_new_bars() == 200
    assert tr.step_new_bars() == 0  # same bars delivered again -> nothing happens
    assert tr.state.bars_processed == 200


def test_gap_is_detected_alerted_and_survived(cfg, tmp_path):
    df = null_market(seed=2, n_bars=400, start="2024-01-01")
    df = df.drop(df.index[150:155])
    alerter = Alerter()
    feed = ReplayFeed(df, 100)  # first 100 bars are warm-up history; the gap (bars 150-154) arrives "live"
    tr = PaperTrader(cfg, make("donchian", n=24, k_atr=3.0, allow_short=True), feed, StateStore(tmp_path), alerter,
                     initial_equity=1.0, lookback_bars=500)
    feed.advance(len(df))
    tr.step_new_bars()
    assert any("data gap: 5 bar" in m for _, m in alerter.sent)
    assert tr.state.bars_processed == len(df) - 100 and not tr.state.halted


def test_reconciliation_mismatch_halts_and_alerts(cfg, tmp_path):
    df = trending_market(seed=6, n_bars=24 * 40, start="2024-01-01")
    alerter = Alerter()
    feed = ReplayFeed(df, 0)
    tr = PaperTrader(cfg, make("donchian", n=24, k_atr=2.0, allow_short=True), feed, StateStore(tmp_path), alerter,
                     initial_equity=1.0, lookback_bars=len(df) + 10)
    feed.advance(300)
    tr.step_new_bars()
    assert not tr.state.halted
    tr.state.realized_net += 0.05  # corrupt the ledger
    feed.advance(10)
    tr.step_new_bars()
    assert tr.state.halted and tr.state.unreconciled_errors >= 1
    assert any(lvl == "critical" and "ledger mismatch" in m for lvl, m in alerter.sent)


def test_kill_switch_and_halt_flatten_paper_position(cfg, tmp_path):
    c = copy.deepcopy(cfg)
    c["risk"]["kill_switch_drawdown"] = 0.002  # trips immediately on a small loss
    df = null_market(seed=3, n_bars=24 * 60, start="2024-01-01")
    alerter = Alerter()
    feed = ReplayFeed(df, 0)
    tr = PaperTrader(c, make("meanrev", lookback=24, z_in=2.0, k_atr=2.0, er_max=1.01), feed, StateStore(tmp_path), alerter,
                     initial_equity=1.0, lookback_bars=len(df) + 10)
    feed.advance(len(df))
    tr.step_new_bars()
    assert any(lvl == "critical" and "KILL SWITCH" in m for lvl, m in alerter.sent)


# ---------------------------------------------------------------- alerts
def test_telegram_alerter_posts_and_never_raises(monkeypatch):
    calls = []

    class R:
        def raise_for_status(self):
            pass

    monkeypatch.setattr("quantbot.execution.alerts.requests.post", lambda url, json, timeout: calls.append((url, json)) or R())
    a = TelegramAlerter(token="TOKEN123", chat_id="42")
    assert a.send("hello", "info")
    assert "botTOKEN123/sendMessage" in calls[0][0] and calls[0][1]["chat_id"] == "42"

    def boom(*a, **k):
        raise RuntimeError("network down")

    monkeypatch.setattr("quantbot.execution.alerts.requests.post", boom)
    assert a.send("again", "critical") is False  # delivery failure is swallowed (trading must not crash on alerts)


def test_telegram_requires_env_credentials(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    with pytest.raises(ValueError):
        TelegramAlerter()


def test_no_secrets_in_source_or_config():
    import pathlib
    import re

    root = pathlib.Path(__file__).resolve().parents[1]
    blob = "".join(p.read_text() for p in list((root / "quantbot").rglob("*.py")) + [root / "config" / "config.yaml"])
    assert not re.search(r"(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9]{16,}", blob, re.I)


# ---------------------------------------------------------------- gate
def write_paper_record(d, cfg, weeks=5, n_trades=30, drift=0.0001, errors=0, strategy=None, bars_missing=0):
    store = StateStore(d)
    n = int(weeks * 7 * 24)
    idx = pd.date_range("2025-01-01", periods=n, freq="1h", tz="UTC")
    eq = 10_000 * (1 + drift) ** np.arange(n)
    pd.DataFrame({"ts": idx, "equity": eq, "units": 0.0, "price": 100.0}).drop(index=range(10, 10 + bars_missing)) \
        .to_csv(store.equity_path, index=False)
    pd.DataFrame({"net": np.ones(n_trades)}).to_csv(store.trades_path, index=False)
    st = TraderState(S=[0.0], initial_equity=10_000.0, unreconciled_errors=errors,
                     strategy=strategy or {"name": "donchian", "params": {"n": 96}})
    store.save(st)


def gated_cfg(cfg):
    c = copy.deepcopy(cfg)
    c["paper"]["strategy"], c["paper"]["params"] = "donchian", {"n": 96}
    c["paper"]["min_weeks"] = 4
    c["live"]["enabled"] = True
    return c


def test_gate_passes_with_good_record_and_blocks_otherwise(cfg, tmp_path, monkeypatch):
    c = gated_cfg(cfg)
    write_paper_record(tmp_path / "ok", c)
    assert paper_gate(c, tmp_path / "ok").ok
    monkeypatch.setenv("LIVE_TRADING_CONFIRM", "YES")
    assert assert_live_allowed(c, tmp_path / "ok").ok
    cases = {
        "short": dict(weeks=2), "few_trades": dict(n_trades=3), "losing": dict(drift=-0.0003),
        "errors": dict(errors=1), "other_strategy": dict(strategy={"name": "meanrev", "params": {}}),
        "gappy": dict(bars_missing=200),
    }
    for name, kw in cases.items():
        write_paper_record(tmp_path / name, c, **kw)
        assert not paper_gate(c, tmp_path / name).ok, name
        with pytest.raises(LiveNotAllowed):
            assert_live_allowed(c, tmp_path / name)


def test_live_needs_config_flag_env_latch_and_paper_record(cfg, tmp_path, monkeypatch):
    c = gated_cfg(cfg)
    write_paper_record(tmp_path / "ok", c)
    monkeypatch.delenv("LIVE_TRADING_CONFIRM", raising=False)
    with pytest.raises(LiveNotAllowed, match="LIVE_TRADING_CONFIRM"):
        assert_live_allowed(c, tmp_path / "ok")
    monkeypatch.setenv("LIVE_TRADING_CONFIRM", "YES")
    c["live"]["enabled"] = False
    with pytest.raises(LiveNotAllowed, match="live.enabled"):
        assert_live_allowed(c, tmp_path / "ok")
    with pytest.raises(LiveNotAllowed, match="no paper-trading record"):
        assert_live_allowed(gated_cfg(cfg), tmp_path / "missing")


# ---------------------------------------------------------------- live trader on a fake exchange
class FakeClient:
    def __init__(self, equity=10_000.0):
        self.equity, self.pos, self.orders, self.cancelled = equity, 0.0, [], 0

    def fetch_equity(self):
        return self.equity

    def fetch_position(self):
        return self.pos

    def market_order(self, side, amount, reduce_only=False):
        self.orders.append(("market", side, amount, reduce_only))
        self.pos += amount if side == "buy" else -amount

    def stop_order(self, side, amount, stop_price):
        self.orders.append(("stop", side, amount, stop_price))

    def cancel_all(self):
        self.cancelled += 1


class ScriptedStrategy:
    """Minimal strategy stub: returns a prepared (target, stop_dist) for the last bar."""
    trail = False
    name = "scripted"
    params = {}

    def __init__(self):
        self.next = (0.0, 100.0)

    def generate(self, df):
        return pd.DataFrame({"target": [self.next[0]] * len(df), "stop_dist": [self.next[1]] * len(df)}, index=df.index)


def make_live(cfg, tmp_path, monkeypatch, client):
    c = gated_cfg(cfg)
    write_paper_record(tmp_path / "paper", c)
    monkeypatch.setenv("LIVE_TRADING_CONFIRM", "YES")
    hist = null_market(seed=1, n_bars=50, start="2025-03-01")
    strat = ScriptedStrategy()
    lt = LiveTrader(c, strat, client, StateStore(tmp_path / "live"), Alerter(), str(tmp_path / "paper"), hist)
    return lt, strat, hist


def next_bar(hist, price):
    ts = hist.index[-1] + pd.Timedelta(hours=1)
    return ts, pd.Series({"open": price, "high": price, "low": price, "close": price, "volume": 1.0, "filled": False, "valid": True})


def test_live_trader_refuses_construction_without_gate(cfg, tmp_path, monkeypatch):
    monkeypatch.delenv("LIVE_TRADING_CONFIRM", raising=False)
    with pytest.raises(LiveNotAllowed):
        LiveTrader(gated_cfg(cfg), ScriptedStrategy(), FakeClient(), StateStore(tmp_path), Alerter(), str(tmp_path / "x"),
                   null_market(seed=1, n_bars=30))


def test_live_trader_sizes_by_risk_places_stop_and_detects_exchange_stop(cfg, tmp_path, monkeypatch):
    cl = FakeClient(10_000.0)
    lt, strat, hist = make_live(cfg, tmp_path, monkeypatch, cl)
    strat.next = (1.0, 200.0)  # long, stop 200 away; price 20000 -> 1% stop; risk 1% of 10k = 100 -> 0.5 units
    ts, row = next_bar(hist, 20_000.0)
    lt.on_bar_close(ts, row)
    kinds = [o[0] for o in cl.orders]
    assert kinds == ["market", "stop"]
    assert cl.orders[0][2] == pytest.approx(0.5) and cl.orders[1][3] == pytest.approx(19_800.0)
    assert cl.orders[1][1] == "sell" and cl.orders[1][1:3] == ("sell", pytest.approx(0.5))
    # exchange fills the stop between bars: position -> 0; bot must notice, not halt, and not re-enter on the same signal
    cl.pos = 0.0
    row2 = row.copy()
    row2[["open", "high", "low", "close"]] = 19_700.0
    lt.on_bar_close(ts + pd.Timedelta(hours=1), row2)
    assert not lt.halted and cl.pos == 0.0 and len(cl.orders) == 2  # noticed the stop-out; blocked from re-entering


def test_live_trader_halts_and_flattens_on_unexplained_mismatch(cfg, tmp_path, monkeypatch):
    cl = FakeClient()
    lt, strat, hist = make_live(cfg, tmp_path, monkeypatch, cl)
    strat.next = (1.0, 200.0)
    ts, row = next_bar(hist, 20_000.0)
    lt.on_bar_close(ts, row)
    cl.pos = 0.9  # exchange shows a different size than the bot believes (manual trade? partial fill?)
    ts2 = ts + pd.Timedelta(hours=1)
    lt.on_bar_close(ts2, row)
    assert lt.halted and cl.pos == pytest.approx(0.0)  # flattened
    n = len(cl.orders)
    lt.on_bar_close(ts2 + pd.Timedelta(hours=1), row)  # halted: no further orders
    assert len(cl.orders) == n


def test_live_trader_kill_switch_on_real_equity(cfg, tmp_path, monkeypatch):
    cl = FakeClient(10_000.0)
    lt, strat, hist = make_live(cfg, tmp_path, monkeypatch, cl)
    ts, row = next_bar(hist, 20_000.0)
    cl.equity = 8_000.0  # 20% below the 10k peak -> kill switch (limit 15%)
    lt.on_bar_close(ts, row)
    assert lt.halted


# ---------------------------------------------------------------- exchange client retry / reconnect
def test_exchange_client_retries_with_backoff_and_reconnects(monkeypatch):
    sleeps = []
    monkeypatch.setattr(exchange_mod.time, "sleep", lambda s: sleeps.append(s))
    cl = exchange_mod.ExchangeClient("binanceusdm", "BTC/USDT:USDT", "1h", sandbox=False, max_retries=5)
    now = 1_700_000_000_000
    rows = [[now - 3 * 3_600_000 + k * 3_600_000, 1, 2, 0.5, 1.5, 10] for k in range(3)]
    state = {"n": 0}

    def flaky(*a, **k):
        state["n"] += 1
        if state["n"] <= 3:
            raise ConnectionError("boom")
        return rows

    monkeypatch.setattr(cl.ex, "fetch_ohlcv", flaky)
    monkeypatch.setattr(cl, "now_ms", lambda: now)
    monkeypatch.setattr(cl, "reconnect", lambda: setattr(cl, "reconnects", cl.reconnects + 1))
    df = cl.fetch_closed_bars()
    assert len(df) == 3 and sleeps == [2.0, 4.0, 8.0] and cl.reconnects == 1  # exponential backoff, reconnect after 3rd failure
    monkeypatch.setattr(cl.ex, "fetch_ohlcv", lambda *a, **k: (_ for _ in ()).throw(ConnectionError("down")))
    with pytest.raises(ConnectionError):
        cl.fetch_closed_bars()


def test_exchange_client_drops_unclosed_bar(monkeypatch):
    cl = exchange_mod.ExchangeClient("binanceusdm", "BTC/USDT:USDT", "1h", sandbox=False)
    now = 1_700_000_000_000 + 30 * 60_000  # 30 minutes into the current hour
    hour = (now // 3_600_000) * 3_600_000
    rows = [[hour - 3_600_000, 1, 2, 0.5, 1.5, 1], [hour, 1, 2, 0.5, 1.5, 1]]  # last bar is still forming
    monkeypatch.setattr(cl.ex, "fetch_ohlcv", lambda *a, **k: rows)
    monkeypatch.setattr(cl, "now_ms", lambda: now)
    df = cl.fetch_closed_bars()
    assert len(df) == 1 and df.index[0] == pd.to_datetime(hour - 3_600_000, unit="ms", utc=True)
