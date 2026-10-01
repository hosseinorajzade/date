"""Run the FULL pipeline on synthetic markets to validate the pipeline itself (never to claim an edge).

  null    : efficient market, zero predictable drift      -> the pipeline should REJECT everything
  planted : persistent OU drift (a real, harvestable edge) -> the pipeline should be able to find it

Results land in reports/synthetic/<scenario>_seed<k>/ and are NOT acceptance evidence.
"""
from __future__ import annotations

import argparse
import copy
import json
import logging
import time

import pandas as pd

from ..config import load_config
from ..data.synthetic import null_market, trending_market
from .pipeline import run_all


def make_provider(cfg: dict, scenario: str, seed: int, years: float, trend_strength: float | None = None):
    n = int(24 * 365 * years)
    syms = cfg["market"]["universe"]

    def provider(sym: str):
        s = seed * 1000 + syms.index(sym)
        if scenario == "null":
            return null_market(seed=s, n_bars=n, start=cfg["market"]["start"]), None
        kw = {} if trend_strength is None else {"trend_strength": trend_strength}
        return trending_market(seed=s, n_bars=n, start=cfg["market"]["start"], **kw), None

    return provider


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", choices=["null", "planted"], required=True)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--years", type=float, default=7.0)
    ap.add_argument("--families", nargs="*", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--trend-strength", type=float, default=None)
    ap.add_argument("--short-splits", action="store_true", help="debug: scale split dates to a short series")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO)
    cfg = load_config()
    if args.short_splits:  # keep proportions 46%/21%/33% of the span
        cfg = copy.deepcopy(cfg)
        start = pd.Timestamp(cfg["market"]["start"])
        cfg["splits"]["train_end"] = str((start + pd.Timedelta(days=365.25 * args.years * 0.62)).date())
        cfg["splits"]["val_end"] = str((start + pd.Timedelta(days=365.25 * args.years * 0.80)).date())
    out = args.out or f"reports/synthetic/{args.scenario}_seed{args.seed}"
    t0 = time.time()
    summary = run_all(cfg, make_provider(cfg, args.scenario, args.seed, args.years, args.trend_strength), out,
                      args.families, label=f"synthetic-{args.scenario}-seed{args.seed}")
    print(json.dumps({k: {"stage": v.get("stage"), "accepted": v["accepted"], "params": v["params"]}
                      for k, v in summary["results"].items()}, indent=1, default=str))
    print("elapsed %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
