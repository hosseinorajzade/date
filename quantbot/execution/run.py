"""CLI:  python -m quantbot.execution.run --mode paper|live [--config config/config.yaml]

paper: runs the PaperTrader against the exchange's closed-bar feed (market data only; no keys needed for public data).
live : refused unless the paper gate passed, config live.enabled, and env LIVE_TRADING_CONFIRM=YES. Use sandbox first.
"""
from __future__ import annotations

import argparse
import logging

from ..config import load_config
from ..strategies.registry import make
from .alerts import build_alerter
from .exchange import ExchangeClient
from .feed import CcxtFeed
from .gate import LiveNotAllowed, assert_live_allowed, paper_gate
from .paper import PaperTrader
from .state import StateStore


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["paper", "live", "gate"], default="paper")
    ap.add_argument("--config", default=None)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    cfg = load_config(args.config)
    p = cfg["paper"]
    if not p.get("strategy"):
        raise SystemExit("config paper.strategy is empty: set it only AFTER a strategy has passed the hold-out acceptance "
                         "(see reports/). Refusing to trade an unvalidated strategy.")
    state_dir = p["state_dir"]
    if args.mode == "gate":
        g = paper_gate(cfg, state_dir)
        print("GATE:", "PASS" if g.ok else "FAIL")
        for k, (ok, d) in g.checks.items():
            print(f"  [{'x' if ok else ' '}] {k}: {d}")
        return
    strat = make(p["strategy"], **p["params"])
    alerter = build_alerter(cfg)
    m = cfg["market"]
    if args.mode == "live":
        try:
            assert_live_allowed(cfg, state_dir)
        except LiveNotAllowed as exc:
            raise SystemExit(str(exc))
        raise SystemExit("live loop intentionally not wired into the CLI: instantiate quantbot.execution.live.LiveTrader "
                         "yourself after reviewing README 'Going live' and a successful TESTNET run.")
    client = ExchangeClient(m["exchange"], m["primary"], m["timeframe"], sandbox=False)  # public market data only
    trader = PaperTrader(cfg, strat, CcxtFeed(client), StateStore(state_dir), alerter)
    trader.run_forever(p["poll_seconds"])


if __name__ == "__main__":
    main()
