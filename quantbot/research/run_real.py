"""Run the full research pipeline on REAL downloaded data.

    python -m quantbot.data.download
    python -m quantbot.research.run_real --out reports/real_run_1

Writes per-family artefacts + report.md under --out and appends every stage to reports/journal.md.
The hold-out is opened at most once per strategy family (HoldoutVault).
"""
from __future__ import annotations

import argparse
import logging

from ..config import load_config
from ..data.store import load_clean, load_funding
from ..reporting.report import run_report
from .pipeline import run_all


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--families", nargs="*", default=None)
    ap.add_argument("--journal", default="reports/journal.md")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO)
    cfg = load_config(args.config)

    def provider(sym):
        df, rep = load_clean(cfg, sym)
        logging.info("%s: %s", sym, rep.as_dict())
        return df, load_funding(cfg, sym)

    run_all(cfg, provider, args.out, args.families, label=args.out.rstrip("/").split("/")[-1], journal_path=args.journal)
    print("report:", run_report(args.out, f"{cfg['market']['primary']} {cfg['market']['timeframe']} research report"))


if __name__ == "__main__":
    main()
