import numpy as np
import pandas as pd
import pytest

from quantbot.backtest.costs import CostModel
from quantbot.backtest.engine import EngineConfig, run_backtest
from quantbot.data.synthetic import null_market
from .conftest import make_bars

NAN = np.nan


def sig(n, **at):
    """Build (target, stop_dist). at={'1': (1.0, 5.0)} means: decision made at close of bar 1, HELD until the
    next listed decision (strategies emit a state, not a one-bar pulse)."""
    t, s = np.zeros(n), np.full(n, 5.0)
    keys = sorted(int(k) for k in at)
    for j, k in enumerate(keys):
        end = keys[j + 1] if j + 1 < len(keys) else n
        t[k:end], s[k:end] = at[str(k)]
    return t, s


def test_no_signal_no_trades_equity_constant(zero_cost_cfg):
    df = make_bars(np.linspace(100, 110, 50))
    r = run_backtest(df, np.zeros(50), np.full(50, 2.0), zero_cost_cfg)
    assert len(r.trades) == 0
    assert (r.equity == 1.0).all()


def test_decision_at_close_t_executes_at_open_t_plus_1(zero_cost_cfg):
    # close[1]=100 but open[2]=103: the fill must be at open[2], never at close[1]
    df = make_bars([100, 100, 103, 104, 105], closes=[100, 100, 103, 104, 105])
    tgt = np.array([0, 1, 1, 1, 1.0])  # decision made at close of bar 1 -> executes at open of bar 2
    r = run_backtest(df, tgt, np.full(5, 5.0), zero_cost_cfg)
    t = r.trades.iloc[0]
    assert t.entry_idx == 2 and t.entry_px == 103.0
    assert t.reason == "end_of_data" or t.reason == "signal"


def test_round_trip_cost_arithmetic_exact(cost_cfg):
    px = 100.0
    df = make_bars([px] * 6)
    tgt, sd = sig(6, **{"1": (1.0, 2.0), "3": (0.0, 2.0)})
    r = run_backtest(df, tgt, sd, cost_cfg)
    t = r.trades.iloc[0]
    units = 1.0 * 0.01 / 2.0  # equity 1.0, risk 1%, stop dist 2 -> 0.005 units
    entry, exit_ = px * (1 + 3e-4), px * (1 - 3e-4)
    expected_fees = 5e-4 * units * (entry + exit_)
    expected_gross = units * (exit_ - entry)
    assert t.units == pytest.approx(units)
    assert t.entry_px == pytest.approx(entry) and t.exit_px == pytest.approx(exit_)
    assert t.fees == pytest.approx(expected_fees)
    assert t.net == pytest.approx(expected_gross - expected_fees)
    assert r.equity.iloc[-1] == pytest.approx(1.0 + t.net)


def test_short_pnl_sign(zero_cost_cfg):
    df = make_bars([100, 100, 100, 90, 90, 90])
    tgt, sd = sig(6, **{"1": (-1.0, 5.0), "3": (0.0, 5.0)})
    r = run_backtest(df, tgt, sd, zero_cost_cfg)
    t = r.trades.iloc[0]
    assert t.side == -1 and t.gross > 0  # short profits when price falls


def test_risk_sizing_loses_exactly_risk_fraction_at_stop(zero_cost_cfg):
    # long from 100, stop 5 below = 95; bar 3 low pierces 95 -> loss must be 1% of equity
    df = make_bars([100, 100, 100, 100, 100], highs=[100] * 5, lows=[100, 100, 100, 94, 100], closes=[100] * 5)
    tgt, sd = sig(5, **{"1": (1.0, 5.0)})
    r = run_backtest(df, tgt, sd, zero_cost_cfg)
    t = r.trades.iloc[0]
    assert t.reason == "stop" and t.exit_px == pytest.approx(95.0)
    assert t.net == pytest.approx(-0.01)
    assert t.r_multiple == pytest.approx(-1.0)


def test_gap_through_stop_fills_at_open(zero_cost_cfg):
    df = make_bars([100, 100, 100, 90, 90], highs=[100, 100, 100, 91, 90], lows=[100, 100, 100, 89, 90],
                   closes=[100, 100, 100, 90, 90])
    tgt, sd = sig(5, **{"1": (1.0, 5.0)})
    r = run_backtest(df, tgt, sd, zero_cost_cfg)
    t = r.trades.iloc[0]
    assert t.reason == "stop" and t.exit_px == pytest.approx(90.0)  # open gapped below the 95 stop
    assert t.r_multiple < -1.5  # gap loss exceeds the planned 1R


def test_stop_slippage_applied_worse_than_normal(cost_cfg):
    df = make_bars([100] * 4, highs=[100] * 4, lows=[100, 100, 94, 100], closes=[100] * 4)
    tgt, sd = sig(4, **{"0": (1.0, 5.0)})
    r = run_backtest(df, tgt, sd, cost_cfg)
    t = r.trades.iloc[0]
    assert t.reason == "stop"
    assert t.exit_px == pytest.approx((100 * (1 + 3e-4) - 5.0) * (1 - 6e-4), rel=1e-6)


def test_no_reentry_on_same_signal_after_stop(zero_cost_cfg):
    low = [100, 100, 94, 100, 100, 100, 100, 100]
    df = make_bars([100] * 8, highs=[100] * 8, lows=low, closes=[100] * 8)
    tgt = np.ones(8)  # signal stays long throughout
    r = run_backtest(df, tgt, np.full(8, 5.0), zero_cost_cfg)
    assert len(r.trades) == 1  # stopped once, never re-enters on the unchanged signal
    # but a fresh signal (0 then 1) does re-enter
    tgt2 = np.array([1, 1, 1, 1, 0, 1, 1, 1.0])
    r2 = run_backtest(df, tgt2, np.full(8, 5.0), zero_cost_cfg)
    assert len(r2.trades) >= 2


def test_funding_sign(zero_cost_cfg):
    df = make_bars([100.0] * 10)
    tgt, sd = sig(10, **{"0": (1.0, 5.0), "8": (0.0, 5.0)})
    long_r = run_backtest(df, tgt, sd, zero_cost_cfg, funding=0.0001)
    tgt_s, _ = sig(10, **{"0": (-1.0, 5.0), "8": (0.0, 5.0)})
    short_r = run_backtest(df, tgt_s, sd, zero_cost_cfg, funding=0.0001)
    assert long_r.trades.funding.iloc[0] < 0  # longs pay positive funding
    assert short_r.trades.funding.iloc[0] > 0  # shorts receive it
    assert long_r.trades.funding.iloc[0] == pytest.approx(-short_r.trades.funding.iloc[0])


def test_max_leverage_cap():
    cfg = EngineConfig(costs=CostModel(0, 0, 0, 0), risk_per_trade=0.5, max_leverage=2.0, min_stop_pct=0.0,
                       daily_loss_limit=1.0, kill_switch_drawdown=1.0)
    df = make_bars([100.0] * 5)
    tgt, sd = sig(5, **{"0": (1.0, 1.0), "3": (0.0, 1.0)})  # uncapped: 0.5/1 = 0.5 units*100 = 50x
    r = run_backtest(df, tgt, sd, cfg)
    assert r.trades.units.iloc[0] * 100 <= 2.0 * 1.0 + 1e-9


def test_min_stop_floor_limits_size():
    cfg = EngineConfig(costs=CostModel(0, 0, 0, 0), risk_per_trade=0.01, max_leverage=100.0, min_stop_pct=0.01,
                       daily_loss_limit=1.0, kill_switch_drawdown=1.0)
    df = make_bars([100.0] * 5)
    tgt, sd = sig(5, **{"0": (1.0, 0.0001), "3": (0.0, 1.0)})
    r = run_backtest(df, tgt, sd, cfg)
    assert r.trades.units.iloc[0] == pytest.approx(0.01 / 1.0)  # stop dist floored to 1% of price = 1.0


def test_daily_loss_limit_flattens_and_blocks_rest_of_day():
    cfg = EngineConfig(costs=CostModel(0, 0, 0, 0), risk_per_trade=0.5, max_leverage=100.0, min_stop_pct=0.0,
                       daily_loss_limit=0.03, kill_switch_drawdown=1.0)
    # bar 2 closes 10% lower -> equity -5%... exceeds 3% limit; position must be closed at next open and
    # no new entry until the next UTC day even though the signal stays long
    n = 60
    o = np.full(n, 100.0)
    c = o.copy()
    o[3:] = 90.0
    c[2:] = 90.0
    c[2] = 90.0
    df = make_bars(o, closes=c, start="2024-01-01 00:00")
    tgt = np.ones(n)
    sd = np.full(n, 50.0)
    r = run_backtest(df, tgt, sd, cfg)
    assert r.n_daily_halts >= 1
    first = r.trades.iloc[0]
    assert first.reason == "daily_limit"
    day0_entries = r.trades[r.trades.entry_time < pd.Timestamp("2024-01-02", tz="UTC")]
    assert len(day0_entries) == 1  # no re-entry later the same UTC day
    assert (r.trades.entry_time >= pd.Timestamp("2024-01-02", tz="UTC")).any() or len(r.trades) == 1


def test_kill_switch_flattens_and_halts_for_cooldown():
    cfg = EngineConfig(costs=CostModel(0, 0, 0, 0), risk_per_trade=0.5, max_leverage=100.0, min_stop_pct=0.0,
                       daily_loss_limit=1.0, kill_switch_drawdown=0.10, kill_cooldown_bars=10)
    n = 40
    o = np.full(n, 100.0)
    c = o.copy()
    c[5:] = 84.0
    o[6:] = 84.0
    df = make_bars(o, closes=c)
    tgt = np.ones(n)
    r = run_backtest(df, tgt, np.full(n, 40.0), cfg)
    assert r.n_kill_events == 1
    assert r.trades.iloc[0].reason == "kill_switch"
    # no trade starts during the cooldown window
    kill_exit = int(r.trades.iloc[0].exit_idx)
    later = r.trades[r.trades.entry_idx > r.trades.iloc[0].entry_idx]
    assert (later.entry_idx >= kill_exit + 10).all()


def test_equity_identity_sum_of_trades(cost_cfg):
    df = null_market(seed=7, n_bars=24 * 90)
    rng = np.random.default_rng(1)
    tgt = rng.choice([-1.0, 0.0, 1.0], size=len(df))
    sd = (df.close * 0.02).to_numpy()
    cfg = EngineConfig(costs=cost_cfg.costs, risk_per_trade=0.01, max_leverage=2.0, daily_loss_limit=1.0,
                       kill_switch_drawdown=1.0)
    r = run_backtest(df, tgt, sd, cfg, funding=0.00001)
    assert r.equity.iloc[-1] == pytest.approx(1.0 + r.trades.net.sum(), rel=1e-9, abs=1e-12)
    assert (r.trades.fees > 0).all()
    assert r.trades.exit_idx.ge(r.trades.entry_idx).all()


def test_engine_has_no_lookahead_future_bars_do_not_change_past_equity(cost_cfg):
    df = null_market(seed=3, n_bars=24 * 60)
    rng = np.random.default_rng(2)
    tgt = rng.choice([-1.0, 0.0, 1.0], size=len(df))
    sd = (df.close * 0.02).to_numpy()
    k = len(df) // 2
    full = run_backtest(df, tgt, sd, cost_cfg)
    df2 = df.copy()
    df2.iloc[k + 1:, :4] = df2.iloc[k + 1:, :4].to_numpy()[::-1] * 3.0  # wreck the future
    tgt2, sd2 = tgt.copy(), sd.copy()
    tgt2[k + 1:] = -tgt2[k + 1:]
    alt = run_backtest(df2, tgt2, sd2, cost_cfg)
    # equity through bar k+1 (bar k+1 executes the decision from bar k, which is unchanged)... compare through k
    assert np.allclose(full.equity.iloc[: k + 1].to_numpy(), alt.equity.iloc[: k + 1].to_numpy(), rtol=0, atol=1e-14)


def test_nan_gap_bars_hold_state_and_do_not_trade(zero_cost_cfg):
    # position opened before the gap; strategies emit target 0 on invalid bars, so the position is closed at the
    # first VALID open after the gap (never "traded" inside it) and equity stays finite throughout
    o = [100, 100, 100, NAN, NAN, 101, 101, 101]
    df = make_bars(o, closes=o, highs=o, lows=o)
    tgt = np.array([1, 1, 1, 0, 0, 0, 0, 0.0])
    r = run_backtest(df, tgt, np.full(8, 5.0), zero_cost_cfg)
    assert np.isfinite(r.equity.to_numpy()).all()
    assert len(r.trades) == 1
    t = r.trades.iloc[0]
    assert t.entry_idx == 1 and t.exit_idx == 5 and t.reason == "signal"


def test_entry_inside_data_gap_is_not_executed(zero_cost_cfg):
    o = [100, 100, NAN, NAN, 100, 100, 100]
    df = make_bars(o, closes=o, highs=o, lows=o)
    tgt = np.array([0, 1, 0, 0, 0, 0, 0.0])  # decision at bar 1 would fill at bar 2 = missing data
    r = run_backtest(df, tgt, np.full(7, 5.0), zero_cost_cfg)
    assert len(r.trades) == 0


def test_trailing_stop_ratchets_up(zero_cost_cfg):
    from dataclasses import replace
    cfg = replace(zero_cost_cfg, trailing=True)
    closes = [100, 100, 110, 120, 130, 125, 120]
    lows = [100, 100, 108, 118, 128, 118, 110]  # bar 5 low 118 < trailed stop (130-5=125) -> exit at 125
    df = make_bars(closes, closes=closes, lows=lows, highs=closes)
    tgt = np.ones(7)
    r = run_backtest(df, tgt, np.full(7, 5.0), cfg)
    t = r.trades.iloc[0]
    assert t.reason == "stop" and t.exit_px == pytest.approx(125.0)


@pytest.mark.slow
@pytest.mark.parametrize("trailing", [False, True])
def test_engine_is_unbiased_on_a_martingale_random_entries_have_zero_mean_R(trailing):
    """Guard against engine-side free lunches (stop fills, sizing, state handling).

    On a MARTINGALE price path with random long/short entries and zero costs, every trade has zero expected P&L
    (optional stopping), so the mean R-multiple must be statistically indistinguishable from 0 for both sides and
    all exit types. A systematic positive mean here means the engine (or the data generator) manufactures edge.
    This test caught a real artefact: coarse intrabar discretisation made stop fills look profitable.
    """
    from dataclasses import replace
    from quantbot.strategies.features import atr

    base = EngineConfig(costs=CostModel(0, 0, 0, 0), daily_loss_limit=1.0, kill_switch_drawdown=1.0)
    cfg = replace(base, trailing=trailing)
    rs = []
    for seed in range(24):
        df = null_market(seed=900 + seed, n_bars=24 * 365 * 2)
        sd = (3.0 * atr(df, 14)).bfill().to_numpy()
        rng = np.random.default_rng(seed)
        tgt = np.zeros(len(df))
        pos = 0.0
        for i in range(len(df)):
            if pos == 0.0 and rng.random() < 0.0045:
                pos = rng.choice([-1.0, 1.0])
            elif pos != 0.0 and rng.random() < 0.02:
                pos = 0.0
            tgt[i] = pos
        t = run_backtest(df, tgt, sd, cfg).trades
        rs.append(t[["side", "r_multiple"]])
    t = pd.concat(rs)
    se = t.r_multiple.std() / np.sqrt(len(t))
    assert len(t) > 1000
    assert abs(t.r_multiple.mean()) < 3.5 * se, (t.r_multiple.mean(), se)
    for side, g in t.groupby("side"):
        assert abs(g.r_multiple.mean()) < 3.5 * g.r_multiple.std() / np.sqrt(len(g)), (side, g.r_multiple.mean())
