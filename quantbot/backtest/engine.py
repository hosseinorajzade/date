"""Event-driven bar engine (numba kernel) shared by backtest and paper trading.

Timing contract (no look-ahead):
  * A strategy emits (target, stop_dist) at the CLOSE of bar t, using data <= t.
  * That decision is executed at the OPEN of bar t+1 (one-bar latency), at open*(1 +/- slippage).
  * Stops are evaluated intrabar using high/low of bars AFTER entry (entry bar included, pessimistic:
    a stop inside the entry bar's range is assumed hit). Gaps through a stop fill at the open.
  * Risk limits (daily loss, kill switch) are evaluated at bar close and acted on at the next open.

Accounting: equity = cash + units*(close - entry_price); fees, slippage and funding are charged
explicitly. Trades carry their own fees/funding so sum(trade net pnl) reconciles to equity.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from numba import njit

from ..risk.sizing import position_size
from .costs import CostModel

# ---- state vector layout -------------------------------------------------------------------
(S_CASH, S_UNITS, S_ENTRY, S_STOP, S_STOPD, S_PEAK, S_DAY, S_DAYEQ, S_HALTDAY, S_KILLUNTIL,
 S_BLOCKDIR, S_TRFEES, S_TRFUND, S_TRIDX, S_TRRISK, S_FLATTEN, S_EXTREME, S_NKILL, S_NDAYHALT,
 S_LASTEQ, S_TRSLIP, S_N) = range(22)
# ---- parameter vector layout ---------------------------------------------------------------
(P_FEE, P_SLIP, P_STOPSLIP, P_RISK, P_MAXLEV, P_MINSTOP, P_DAYLOSS, P_KILLDD, P_COOLDOWN,
 P_TRAIL, P_N) = range(11)
# ---- trade record layout -------------------------------------------------------------------
(T_ENTRY, T_EXIT, T_SIDE, T_UNITS, T_ENTRYPX, T_EXITPX, T_GROSS, T_FEES, T_FUND, T_NET,
 T_REASON, T_RISK, T_N) = range(13)
R_SIGNAL, R_STOP, R_DAYLIMIT, R_KILL, R_END = 0, 1, 2, 3, 4
REASONS = {0: "signal", 1: "stop", 2: "daily_limit", 3: "kill_switch", 4: "end_of_data"}


@dataclass(frozen=True)
class EngineConfig:
    costs: CostModel = field(default_factory=CostModel)
    risk_per_trade: float = 0.01
    max_leverage: float = 2.0
    min_stop_pct: float = 0.003
    daily_loss_limit: float = 0.03
    kill_switch_drawdown: float = 0.15
    kill_cooldown_bars: int = 24 * 14
    trailing: bool = False
    initial_equity: float = 1.0

    @classmethod
    def from_config(cls, cfg: dict, trailing: bool = False) -> "EngineConfig":
        from ..config import bars_per_day

        r = cfg["risk"]
        return cls(
            costs=CostModel.from_config(cfg),
            risk_per_trade=r["risk_per_trade"], max_leverage=r["max_leverage"],
            min_stop_pct=r["min_stop_pct"], daily_loss_limit=r["daily_loss_limit"],
            kill_switch_drawdown=r["kill_switch_drawdown"],
            kill_cooldown_bars=int(r["kill_cooldown_days"] * bars_per_day(cfg["market"]["timeframe"])),
            trailing=trailing,
        )

    def with_costs(self, costs: CostModel) -> "EngineConfig":
        from dataclasses import replace
        return replace(self, costs=costs)

    def param_vector(self) -> np.ndarray:
        p = np.zeros(P_N)
        p[P_FEE], p[P_SLIP], p[P_STOPSLIP] = self.costs.fee, self.costs.slip, self.costs.stop_slip
        p[P_RISK], p[P_MAXLEV], p[P_MINSTOP] = self.risk_per_trade, self.max_leverage, self.min_stop_pct
        p[P_DAYLOSS], p[P_KILLDD], p[P_COOLDOWN] = self.daily_loss_limit, self.kill_switch_drawdown, self.kill_cooldown_bars
        p[P_TRAIL] = 1.0 if self.trailing else 0.0
        return p


def new_state(initial_equity: float = 1.0) -> np.ndarray:
    s = np.zeros(S_N)
    s[S_CASH] = initial_equity
    s[S_PEAK] = initial_equity
    s[S_DAY] = -1
    s[S_DAYEQ] = initial_equity
    s[S_LASTEQ] = initial_equity
    s[S_KILLUNTIL] = -1
    return s


@njit(cache=True)
def _record_exit(S, P, trades, ntr, i, fill_px, reason):
    """Close the open position at fill_px (already slippage-adjusted). Returns new trade count."""
    units = S[S_UNITS]
    fee = P[P_FEE] * abs(units) * fill_px
    gross = units * (fill_px - S[S_ENTRY])
    S[S_CASH] += gross - fee
    S[S_TRFEES] += fee
    net = gross - S[S_TRFEES] + S[S_TRFUND]
    trades[ntr, T_ENTRY] = S[S_TRIDX]
    trades[ntr, T_EXIT] = i
    trades[ntr, T_SIDE] = 1.0 if units > 0 else -1.0
    trades[ntr, T_UNITS] = abs(units)
    trades[ntr, T_ENTRYPX] = S[S_ENTRY]
    trades[ntr, T_EXITPX] = fill_px
    trades[ntr, T_GROSS] = gross
    trades[ntr, T_FEES] = S[S_TRFEES]
    trades[ntr, T_FUND] = S[S_TRFUND]
    trades[ntr, T_NET] = net
    trades[ntr, T_REASON] = reason
    trades[ntr, T_RISK] = S[S_TRRISK]
    S[S_UNITS] = 0.0
    S[S_TRFEES] = 0.0
    S[S_TRFUND] = 0.0
    S[S_STOP] = 0.0
    return ntr + 1


@njit(cache=True)
def step(S, P, i, o, h, l, c, prev_tgt, prev_stopd, funding, day_id, trades, ntr):
    """Advance the engine by one bar. Returns (equity_at_close, new_trade_count).

    prev_tgt/prev_stopd are the decision made at the close of bar i-1 (NaN target = no information).
    """
    if math.isnan(c) or math.isnan(o):  # unfilled data gap: hold state, mark nothing
        return S[S_LASTEQ], ntr

    # new UTC day: reset the daily loss reference
    if day_id != S[S_DAY]:
        S[S_DAY] = day_id
        S[S_DAYEQ] = S[S_CASH] + S[S_UNITS] * (o - S[S_ENTRY]) if S[S_UNITS] != 0.0 else S[S_CASH]
        S[S_HALTDAY] = 0.0
    # kill-switch cooldown elapsed: operator re-arms with a fresh peak
    if S[S_KILLUNTIL] >= 0 and i == S[S_KILLUNTIL]:
        S[S_PEAK] = S[S_CASH] + (S[S_UNITS] * (o - S[S_ENTRY]) if S[S_UNITS] != 0.0 else 0.0)

    killed = i < S[S_KILLUNTIL]
    halted = killed or S[S_HALTDAY] > 0.0

    # ---------------- decisions executed at the open ----------------
    tgt = prev_tgt
    if math.isnan(tgt):
        tgt = 0.0
    desired = 0.0
    if tgt > 0.0:
        desired = 1.0
    elif tgt < 0.0:
        desired = -1.0
    conviction = abs(tgt)
    if halted:
        desired = 0.0
    if S[S_BLOCKDIR] != 0.0 and desired != S[S_BLOCKDIR]:
        S[S_BLOCKDIR] = 0.0  # signal moved on since the stop-out: re-arm
    if desired != 0.0 and desired == S[S_BLOCKDIR] and S[S_UNITS] == 0.0:
        desired = 0.0  # still the same signal that was stopped out: wait for a fresh one

    flatten_reason = R_SIGNAL
    force_flat = S[S_FLATTEN] > 0.0
    if force_flat:
        flatten_reason = int(S[S_FLATTEN]) + 1  # 1 -> daily_limit(2), 2 -> kill(3)
        S[S_FLATTEN] = 0.0
        desired = 0.0

    if S[S_UNITS] != 0.0:
        cur = 1.0 if S[S_UNITS] > 0 else -1.0
        if desired != cur:
            px = o * (1.0 - P[P_SLIP]) if cur > 0 else o * (1.0 + P[P_SLIP])
            ntr = _record_exit(S, P, trades, ntr, i, px, flatten_reason if force_flat else R_SIGNAL)

    if S[S_UNITS] == 0.0 and desired != 0.0 and not math.isnan(prev_stopd):
        equity_now = S[S_CASH]
        units = position_size(equity_now, o, prev_stopd, conviction, P[P_RISK], P[P_MAXLEV], P[P_MINSTOP])
        if units > 0.0:
            sd = max(prev_stopd, P[P_MINSTOP] * o)
            px = o * (1.0 + P[P_SLIP]) if desired > 0 else o * (1.0 - P[P_SLIP])
            fee = P[P_FEE] * units * px
            S[S_CASH] -= fee
            S[S_TRFEES] = fee
            S[S_TRFUND] = 0.0
            S[S_UNITS] = desired * units
            S[S_ENTRY] = px
            S[S_STOPD] = sd
            S[S_STOP] = px - desired * sd
            S[S_EXTREME] = px
            S[S_TRIDX] = i
            S[S_TRRISK] = units * sd
            S[S_BLOCKDIR] = 0.0

    # ---------------- intrabar stop ----------------
    if S[S_UNITS] != 0.0:
        if S[S_UNITS] > 0.0 and l <= S[S_STOP]:
            fill = min(S[S_STOP], o) * (1.0 - P[P_STOPSLIP])
            ntr = _record_exit(S, P, trades, ntr, i, fill, R_STOP)
            S[S_BLOCKDIR] = 1.0
        elif S[S_UNITS] < 0.0 and h >= S[S_STOP]:
            fill = max(S[S_STOP], o) * (1.0 + P[P_STOPSLIP])
            ntr = _record_exit(S, P, trades, ntr, i, fill, R_STOP)
            S[S_BLOCKDIR] = -1.0

    # ---------------- funding (position held through the bar) ----------------
    if S[S_UNITS] != 0.0:
        f = -S[S_UNITS] * c * funding  # longs pay when funding > 0
        S[S_CASH] += f
        S[S_TRFUND] += f
        if P[P_TRAIL] > 0.0:  # ratchet the stop with favourable closes (effective from next bar)
            if S[S_UNITS] > 0.0:
                S[S_EXTREME] = max(S[S_EXTREME], c)
                S[S_STOP] = max(S[S_STOP], S[S_EXTREME] - S[S_STOPD])
            else:
                S[S_EXTREME] = min(S[S_EXTREME], c)
                S[S_STOP] = min(S[S_STOP], S[S_EXTREME] + S[S_STOPD])

    # ---------------- mark to market + risk limits ----------------
    equity = S[S_CASH] + (S[S_UNITS] * (c - S[S_ENTRY]) if S[S_UNITS] != 0.0 else 0.0)
    if equity > S[S_PEAK]:
        S[S_PEAK] = equity
    if i >= S[S_KILLUNTIL] and equity <= S[S_PEAK] * (1.0 - P[P_KILLDD]):
        S[S_KILLUNTIL] = i + 1 + P[P_COOLDOWN]
        S[S_NKILL] += 1.0
        if S[S_UNITS] != 0.0:
            S[S_FLATTEN] = 2.0  # -> reason code 3 (kill_switch)
    if S[S_HALTDAY] == 0.0 and equity <= S[S_DAYEQ] * (1.0 - P[P_DAYLOSS]):
        S[S_HALTDAY] = 1.0
        S[S_NDAYHALT] += 1.0
        if S[S_UNITS] != 0.0 and S[S_FLATTEN] == 0.0:
            S[S_FLATTEN] = 1.0  # -> reason code 2 (daily_limit)
    S[S_LASTEQ] = equity
    return equity, ntr


@njit(cache=True)
def _run(o, h, l, c, tgt, stopd, funding, day_id, P, init_equity, init_tgt, init_stopd):
    n = len(c)
    S = np.zeros(S_N)
    S[S_CASH] = init_equity
    S[S_PEAK] = init_equity
    S[S_DAY] = -1.0
    S[S_DAYEQ] = init_equity
    S[S_LASTEQ] = init_equity
    S[S_KILLUNTIL] = -1.0
    trades = np.zeros((n + 2, T_N))
    equity = np.empty(n)
    units = np.empty(n)
    ntr = 0
    pt = init_tgt
    ps = init_stopd
    for i in range(n):
        eq, ntr = step(S, P, i, o[i], h[i], l[i], c[i], pt, ps, funding[i], day_id[i], trades, ntr)
        equity[i] = eq
        units[i] = S[S_UNITS]
        pt = tgt[i]
        ps = stopd[i]
    if S[S_UNITS] != 0.0:  # liquidate at the final close so every trade is realised and costed
        last = n - 1
        px = c[last] * (1.0 - P[P_SLIP]) if S[S_UNITS] > 0 else c[last] * (1.0 + P[P_SLIP])
        ntr = _record_exit(S, P, trades, ntr, last, px, R_END)
        equity[last] = S[S_CASH]
        units[last] = 0.0
    return equity, units, trades[:ntr], S


@dataclass
class BacktestResult:
    equity: pd.Series
    position: pd.Series
    trades: pd.DataFrame
    n_kill_events: int
    n_daily_halts: int
    config: EngineConfig

    @property
    def returns(self) -> pd.Series:
        return self.equity.pct_change().fillna(self.equity.iloc[0] / self.config.initial_equity - 1.0)


def run_backtest(df: pd.DataFrame, target: pd.Series | np.ndarray, stop_dist: pd.Series | np.ndarray,
                 cfg: EngineConfig | None = None, funding: pd.Series | np.ndarray | float = 0.0,
                 init_target: float = 0.0, init_stop_dist: float = np.nan) -> BacktestResult:
    """Run the engine over `df` (columns open/high/low/close, UTC DatetimeIndex).

    `target[t]`/`stop_dist[t]` are the decision made at the close of bar t. `init_*` carry the
    decision made at the close of the bar *before* df[0] (used when slicing a longer series).
    `funding` is the per-bar funding rate (fraction of notional).
    """
    cfg = cfg or EngineConfig()
    n = len(df)
    tgt = np.asarray(target, dtype=np.float64)
    sd = np.asarray(stop_dist, dtype=np.float64)
    if len(tgt) != n or len(sd) != n:
        raise ValueError("signal length must equal number of bars")
    fund = np.full(n, float(funding)) if np.isscalar(funding) else np.asarray(funding, dtype=np.float64)
    if len(fund) != n:
        raise ValueError("funding length must equal number of bars")
    day_id = np.floor(df.index.asi8 / _ticks_per_day(df.index)).astype(np.float64)
    equity, units, trades, S = _run(
        df["open"].to_numpy(np.float64), df["high"].to_numpy(np.float64), df["low"].to_numpy(np.float64),
        df["close"].to_numpy(np.float64), tgt, sd, np.nan_to_num(fund), day_id, cfg.param_vector(),
        float(cfg.initial_equity), float(init_target), float(init_stop_dist))
    tr = pd.DataFrame(trades, columns=["entry_idx", "exit_idx", "side", "units", "entry_px", "exit_px", "gross",
                                       "fees", "funding", "net", "reason", "risk"])
    if len(tr):
        tr["entry_idx"] = tr["entry_idx"].astype(int)
        tr["exit_idx"] = tr["exit_idx"].astype(int)
        tr["entry_time"] = df.index[tr["entry_idx"].to_numpy()]
        tr["exit_time"] = df.index[tr["exit_idx"].to_numpy()]
        tr["reason"] = tr["reason"].astype(int).map(REASONS)
        tr["r_multiple"] = tr["net"] / tr["risk"].replace(0, np.nan)
        tr["bars_held"] = tr["exit_idx"] - tr["entry_idx"]
    return BacktestResult(pd.Series(equity, index=df.index, name="equity"),
                          pd.Series(units, index=df.index, name="units"), tr,
                          int(S[S_NKILL]), int(S[S_NDAYHALT]), cfg)


def _ticks_per_day(index: pd.DatetimeIndex) -> int:
    unit = getattr(index, "unit", "ns")
    return 86_400 * {"s": 1, "ms": 10**3, "us": 10**6, "ns": 10**9}[unit]
