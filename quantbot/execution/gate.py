"""Gate between paper and live trading. Live is refused unless EVERY condition holds."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from ..config import timeframe_to_minutes
from .state import StateStore


class LiveNotAllowed(RuntimeError):
    pass


@dataclass
class GateResult:
    ok: bool
    reasons: list[str] = field(default_factory=list)
    checks: dict = field(default_factory=dict)


def paper_gate(cfg: dict, state_dir: str | Path) -> GateResult:
    g, store = cfg["paper_gate"], StateStore(state_dir)
    res = GateResult(True)

    def need(name: str, ok: bool, detail: str) -> None:
        res.checks[name] = (bool(ok), detail)
        if not ok:
            res.ok = False
            res.reasons.append(f"{name}: {detail}")

    st = store.load()
    if st is None or not store.equity_path.exists():
        return GateResult(False, ["no paper-trading record found"])
    eq = pd.read_csv(store.equity_path, parse_dates=["ts"])
    tr = pd.read_csv(store.trades_path) if store.trades_path.exists() else pd.DataFrame()
    weeks = (eq["ts"].iloc[-1] - eq["ts"].iloc[0]).total_seconds() / (7 * 86400)
    need("duration", weeks >= cfg["paper"]["min_weeks"], f"{weeks:.1f} weeks of paper trading (need {cfg['paper']['min_weeks']})")
    expected = (eq["ts"].iloc[-1] - eq["ts"].iloc[0]) / pd.Timedelta(minutes=timeframe_to_minutes(cfg["market"]["timeframe"])) + 1
    cov = len(eq) / max(expected, 1)
    need("uptime", cov >= g["min_bar_coverage"], f"bar coverage {cov:.3f} (need {g['min_bar_coverage']})")
    need("trades", len(tr) >= g["min_trades"], f"{len(tr)} closed trades (need {g['min_trades']})")
    ret = eq["equity"].iloc[-1] / st.initial_equity - 1
    need("net_return", ret >= g["min_net_return"], f"paper net return {ret:+.3%}")
    mdd = float(np.max(1 - eq["equity"] / eq["equity"].cummax()))
    need("drawdown", mdd <= g["max_drawdown"], f"paper max drawdown {mdd:.2%} (limit {g['max_drawdown']:.0%})")
    need("reconciliation", st.unreconciled_errors <= g["max_unreconciled_errors"],
         f"{st.unreconciled_errors} unreconciled errors")
    want = cfg["paper"].get("strategy")
    need("strategy_unchanged", bool(want) and st.strategy.get("name") == want
         and st.strategy.get("params") == cfg["paper"].get("params"),
         f"paper-traded {st.strategy} vs configured {want} {cfg['paper'].get('params')}")
    return res


def assert_live_allowed(cfg: dict, state_dir: str | Path) -> GateResult:
    reasons = []
    if not cfg.get("live", {}).get("enabled"):
        reasons.append("config live.enabled is false")
    if os.environ.get("LIVE_TRADING_CONFIRM") != "YES":
        reasons.append("env LIVE_TRADING_CONFIRM != YES")
    gate = paper_gate(cfg, state_dir)
    reasons += gate.reasons
    if reasons:
        raise LiveNotAllowed("live trading refused: " + "; ".join(reasons))
    return gate
