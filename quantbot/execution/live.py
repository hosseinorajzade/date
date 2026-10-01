"""Live trader (exchange orders). GATED: cannot even be constructed unless the paper-trading gate has passed.

!! NOT validated against a real exchange in this build. Run on the exchange TESTNET (live.sandbox: true) first. !!

Per closed bar: reconcile exchange position vs belief -> apply risk limits on REAL equity -> compute decision with the
same strategy/sizing code as research -> trade the difference with a reduce-only exchange-side stop attached.
Any unexplained position mismatch halts the bot (and flattens), never "fixes" itself silently.
"""
from __future__ import annotations

import logging
import math

import pandas as pd

from ..risk.sizing import position_size
from ..strategies.base import Strategy
from .alerts import Alerter
from .gate import assert_live_allowed
from .state import StateStore

log = logging.getLogger("live")


class LiveTrader:
    def __init__(self, cfg: dict, strategy: Strategy, client, store: StateStore, alerter: Alerter, paper_state_dir: str,
                 history: pd.DataFrame):
        assert_live_allowed(cfg, paper_state_dir)  # raises LiveNotAllowed
        self.cfg, self.strategy, self.client, self.store, self.alerter = cfg, strategy, client, store, alerter
        r = cfg["risk"]
        self.risk, self.maxlev, self.minstop = r["risk_per_trade"], r["max_leverage"], r["min_stop_pct"]
        self.daily_limit, self.kill_dd = r["daily_loss_limit"], r["kill_switch_drawdown"]
        self.tol = cfg["live"]["max_position_mismatch_pct"] / 100.0
        self.window = history
        self.believed = 0.0
        self.stop_price = float("nan")
        self.blocked_dir = 0.0
        self.peak = client.fetch_equity()
        self.day = None
        self.day_start_equity = self.peak
        self.halted = False
        self.extreme = float("nan")

    def halt(self, reason: str) -> None:
        self.halted = True
        self.alerter.send(f"LIVE HALT: {reason}", "critical")
        try:
            self.client.cancel_all()
            pos = self.client.fetch_position()
            if pos != 0:
                self.client.market_order("sell" if pos > 0 else "buy", abs(pos), reduce_only=True)
        finally:
            self.believed = 0.0

    def on_bar_close(self, ts: pd.Timestamp, row) -> None:
        self.window = pd.concat([self.window, row.to_frame().T.set_axis([ts])]).astype(float).tail(len(self.window) + 1)
        if self.halted:
            return
        equity, pos = self.client.fetch_equity(), self.client.fetch_position()
        # --- reconciliation
        if self.believed != 0.0 and pos == 0.0:  # exchange-side stop filled between bars
            self.blocked_dir = 1.0 if self.believed > 0 else -1.0
            self.alerter.send(f"stop executed on exchange ({self.believed:+.6f})", "warning")
            self.believed = 0.0
        elif abs(pos - self.believed) > self.tol * max(abs(self.believed), 1e-12) + 1e-12:
            return self.halt(f"position mismatch: exchange {pos:+.6f} vs bot {self.believed:+.6f}")
        # --- risk limits on real equity
        day = ts.floor("D")
        if day != self.day:
            self.day, self.day_start_equity = day, equity
        self.peak = max(self.peak, equity)
        if equity <= self.peak * (1 - self.kill_dd):
            return self.halt(f"kill switch: equity {equity:.2f} is >{self.kill_dd:.0%} below peak {self.peak:.2f}")
        day_halt = equity <= self.day_start_equity * (1 - self.daily_limit)
        # --- decision (identical code path to research)
        sig = self.strategy.generate(self.window)
        tgt, sd = float(sig["target"].iloc[-1]), float(sig["stop_dist"].iloc[-1])
        direction = 0.0 if (day_halt or math.isnan(tgt)) else (1.0 if tgt > 0 else -1.0 if tgt < 0 else 0.0)
        if self.blocked_dir != 0.0 and direction != self.blocked_dir:
            self.blocked_dir = 0.0
        if direction == self.blocked_dir and self.believed == 0.0:
            direction = 0.0
        price = float(row["close"])
        if self.believed != 0.0 and math.copysign(1, self.believed) == direction:
            if self.strategy.trail and not math.isnan(self.stop_price):  # ratchet exchange-side stop
                self.extreme = max(self.extreme, price) if direction > 0 else min(self.extreme, price)
                new_stop = self.extreme - sd * direction
                if (direction > 0 and new_stop > self.stop_price) or (direction < 0 and new_stop < self.stop_price):
                    self.client.cancel_all()
                    self.client.stop_order("sell" if direction > 0 else "buy", abs(self.believed), new_stop)
                    self.stop_price = new_stop
            return
        if self.believed != 0.0:  # close the old position
            self.client.cancel_all()
            self.client.market_order("sell" if self.believed > 0 else "buy", abs(self.believed), reduce_only=True)
            self.believed, self.stop_price = 0.0, float("nan")
        if direction != 0.0 and not math.isnan(sd):
            units = position_size(equity, price, sd, abs(tgt), self.risk, self.maxlev, self.minstop)
            if units > 0:
                sdist = max(sd, self.minstop * price)
                self.client.market_order("buy" if direction > 0 else "sell", units)
                self.stop_price = price - direction * sdist
                self.client.stop_order("sell" if direction > 0 else "buy", units, self.stop_price)
                self.believed, self.extreme = direction * units, price
                self.alerter.send(f"LIVE opened {'LONG' if direction > 0 else 'SHORT'} {units:.6f} ~{price:.2f} "
                                  f"stop {self.stop_price:.2f}")
