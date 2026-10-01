"""Paper trader: runs the SAME compiled engine kernel (`backtest.engine.step`) bar by bar on live/replayed data.

Fill model = backtest model: the decision made at the close of bar t is filled at the open of bar t+1 (+ slippage,
fees), stops are evaluated against the high/low of the bars that follow. Bookkeeping therefore lags the market by
one bar (bar t+1 is processed when it closes) but fill PRICES are identical to what the backtest assumes, so paper
results are directly comparable with research results. Differences to a real exchange (queue position, partial
fills, real funding) are exactly what paper trading is meant to expose via the logged fills.

Robustness: atomic state persistence, idempotent bar processing (re-delivered bars are ignored), gap detection and
catch-up, reconnect/backoff in the feed layer, ledger-vs-engine reconciliation after every bar, stale-feed alerts,
kill-switch / daily-limit alerts.
"""
from __future__ import annotations

import logging
import math
import time
from pathlib import Path

import numpy as np
import pandas as pd

from ..backtest.engine import (REASONS, S_CASH, S_NDAYHALT, S_NKILL, S_TRFEES, S_TRFUND, S_TRIDX, S_UNITS, T_N,
                               EngineConfig, new_state, step)
from ..config import timeframe_to_minutes
from ..data.store import funding_per_bar  # noqa: F401  (re-exported for callers building funding series)
from ..strategies.base import Strategy
from .alerts import Alerter
from .feed import BarFeed
from .state import StateStore, TraderState

log = logging.getLogger("paper")


class PaperTrader:
    def __init__(self, cfg: dict, strategy: Strategy, feed: BarFeed, store: StateStore, alerter: Alerter | None = None,
                 initial_equity: float = 10_000.0, lookback_bars: int | None = None, funding_per_bar_rate: float | None = None,
                 symbol: str | None = None):
        self.cfg, self.strategy, self.feed, self.store = cfg, strategy, feed, store
        self.alerter = alerter or Alerter()
        self.symbol = symbol or cfg["market"]["primary"]
        self.tf_min = timeframe_to_minutes(cfg["market"]["timeframe"])
        self.engine_cfg = EngineConfig.from_config(cfg, trailing=strategy.trail)
        self.P = self.engine_cfg.param_vector()
        bars_per_8h = 480.0 / self.tf_min
        self.funding = funding_per_bar_rate if funding_per_bar_rate is not None else \
            cfg["costs"]["funding_bps_per_8h"] * 1e-4 / bars_per_8h
        self.lookback = lookback_bars or max(strategy.warmup_bars() * 3, 3000)
        self.window = pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
        self.state: TraderState = store.load() or self._fresh(initial_equity)
        self._seen_kill = int(self.state.S_arr[S_NKILL])
        self._seen_halt = int(self.state.S_arr[S_NDAYHALT])
        self._bootstrap()

    # ------------------------------------------------------------------ setup
    def _fresh(self, equity: float) -> TraderState:
        st = TraderState(S=new_state(equity).tolist(), initial_equity=equity,
                         strategy={"name": self.strategy.name, "params": self.strategy.params, "symbol": self.symbol})
        return st

    def _bootstrap(self) -> None:
        """Load history so indicators are warm. On a brand-new state the decision at the last historical bar becomes pending."""
        hist = self.feed.history(self.lookback)
        if self.state.last_bar is not None:  # resuming after a restart: window = history up to the last processed bar
            hist = hist[hist.index <= pd.Timestamp(self.state.last_bar)]
        self.window = hist.copy()
        if self.state.last_bar is None and len(hist):
            self.state.last_bar = str(hist.index[-1])
            self.state.first_bar = None  # paper clock starts at the first bar processed live
            self.state.pending_tgt, self.state.pending_sd = self._decision()
            self.store.event(f"bootstrapped on {len(hist)} historical bars; pending decision "
                             f"({self.state.pending_tgt}, {self.state.pending_sd})")
            self.store.save(self.state)

    def _decision(self) -> tuple[float, float]:
        if self.state.halted or len(self.window) < 2:
            return 0.0, float("nan")
        sig = self.strategy.generate(self.window)
        return float(sig["target"].iloc[-1]), float(sig["stop_dist"].iloc[-1])

    # ------------------------------------------------------------------ core
    def process_bar(self, ts: pd.Timestamp, row) -> float:
        st = self.state
        S = st.S_arr
        buf = np.zeros((4, T_N))
        day_id = float(math.floor(ts.timestamp() / 86400.0))
        pending_tgt = 0.0 if st.halted else st.pending_tgt
        eq, ntr = step(S, self.P, st.i, float(row["open"]), float(row["high"]), float(row["low"]), float(row["close"]),
                       pending_tgt, st.pending_sd, self.funding, day_id, buf, 0)
        ts_s = str(ts)
        for k in range(ntr):
            t = buf[k]
            entry_ts = ts_s if int(t[0]) == st.i else (st.entry_ts or ts_s)
            self.store.log_trade([entry_ts, ts_s, int(t[2]), t[3], t[4], t[5], t[6], t[7], t[8], t[9],
                                  REASONS[int(t[10])], t[11]])
            st.realized_net += float(t[9])
            st.n_trades += 1
            self.alerter.send(f"{self.symbol} closed {'LONG' if t[2] > 0 else 'SHORT'} {t[3]:.6f} @ {t[5]:.2f} "
                              f"net {t[9]:+.2f} ({REASONS[int(t[10])]})", dedupe_key=f"trade{st.n_trades}")
        if S[S_UNITS] != 0.0 and int(S[S_TRIDX]) == st.i:
            st.entry_ts = ts_s
            self.alerter.send(f"{self.symbol} opened {'LONG' if S[S_UNITS] > 0 else 'SHORT'} {abs(S[S_UNITS]):.6f} "
                              f"@ bar open {row['open']:.2f}", dedupe_key=f"open{st.i}")
        if S[S_UNITS] == 0.0:
            st.entry_ts = None
        if int(S[S_NKILL]) > self._seen_kill:
            self._seen_kill = int(S[S_NKILL])
            self.alerter.send(f"KILL SWITCH tripped on {self.symbol}: flattening and halting for the cooldown", "critical")
        if int(S[S_NDAYHALT]) > self._seen_halt:
            self._seen_halt = int(S[S_NDAYHALT])
            self.alerter.send(f"daily loss limit hit on {self.symbol}: flat until next UTC day", "warning")
        st.S = S.tolist()
        st.i += 1
        st.bars_processed += 1
        st.last_bar = ts_s
        st.first_bar = st.first_bar or ts_s
        self.store.log_equity(ts_s, eq, S[S_UNITS], float(row["close"]))
        self._reconcile(eq)
        return eq

    def _reconcile(self, eq: float) -> None:
        """Ledger vs engine: cash must equal initial + closed-trade P&L + open-trade (funding - entry fee)."""
        S = self.state.S_arr
        open_part = (S[S_TRFUND] - S[S_TRFEES]) if S[S_UNITS] != 0.0 else 0.0
        expected = self.state.initial_equity + self.state.realized_net + open_part
        if abs(S[S_CASH] - expected) > 1e-7 * max(self.state.initial_equity, 1.0) + 1e-9:
            self.state.unreconciled_errors += 1
            self.state.halted = True
            self.state.halt_reason = f"ledger mismatch: engine cash {S[S_CASH]:.8f} vs ledger {expected:.8f}"
            self.alerter.send(self.state.halt_reason + " — HALTED", "critical")

    # ------------------------------------------------------------------ driver
    def step_new_bars(self) -> int:
        """Process every newly closed bar in order; returns number processed."""
        last = pd.Timestamp(self.state.last_bar) if self.state.last_bar else None
        bars = self.feed.new_bars(last)
        n = 0
        for ts, row in bars.iterrows():
            if last is not None and ts <= last:
                continue  # idempotent: redelivered bar
            if last is not None:
                missed = int((ts - last) / pd.Timedelta(minutes=self.tf_min)) - 1
                if missed > 0:
                    msg = f"data gap: {missed} bar(s) missing before {ts}"
                    self.store.event(msg)
                    self.alerter.send(msg, "warning", dedupe_key=f"gap{ts}")
            self.process_bar(ts, row)
            self.window = pd.concat([self.window, row.to_frame().T.set_axis([ts])]).tail(self.lookback) \
                if len(self.window) else row.to_frame().T.set_axis([ts])
            self.window = self.window.astype(float)
            self.window.index.name = "ts"
            self.state.pending_tgt, self.state.pending_sd = self._decision()
            self.store.save(self.state)
            last = ts
            n += 1
        return n

    def status(self) -> dict:
        S = self.state.S_arr
        return {"last_bar": self.state.last_bar, "bars": self.state.bars_processed, "trades": self.state.n_trades,
                "units": float(S[S_UNITS]), "cash": float(S[S_CASH]), "halted": self.state.halted,
                "halt_reason": self.state.halt_reason, "errors": self.state.unreconciled_errors}

    def run_forever(self, poll_seconds: float = 20.0, stale_factor: float = 2.5, max_consecutive_errors: int = 20,
                    should_stop=lambda: False) -> None:
        consecutive = 0
        self.alerter.send(f"paper trader started: {self.strategy} on {self.symbol}")
        while not should_stop():
            try:
                self.step_new_bars()
                consecutive = 0
                if self.state.last_bar:
                    age = (pd.Timestamp.now(tz="UTC") - pd.Timestamp(self.state.last_bar)).total_seconds() / 60.0
                    if age > stale_factor * self.tf_min:
                        self.alerter.send(f"feed stale: last bar {self.state.last_bar} ({age:.0f} min ago)", "error",
                                          dedupe_key="stale")
            except ConnectionError as exc:
                consecutive += 1
                self.alerter.send(f"connection problem: {exc}", "error", dedupe_key="conn")
            except Exception as exc:  # noqa: BLE001
                consecutive += 1
                log.exception("unexpected error")
                self.alerter.send(f"unexpected error: {exc!r}", "error", dedupe_key=repr(exc))
            if consecutive >= max_consecutive_errors:
                self.state.halted, self.state.halt_reason = True, "too many consecutive errors"
                self.store.save(self.state)
                self.alerter.send("too many consecutive errors — trader HALTED", "critical")
                break
            time.sleep(min(poll_seconds * (1 + consecutive), 300))
