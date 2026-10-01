"""Aggregate all reports/synthetic/*/summary.json into one table (pipeline-validation evidence)."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .report import md_table


def build(root: str | Path = "reports/synthetic") -> Path:
    root = Path(root)
    rows = []
    for d in sorted(root.glob("*_seed*")):
        if not (d / "summary.json").exists():
            continue
        scen = d.name.rsplit("_seed", 1)[0]
        s = json.loads((d / "summary.json").read_text())
        for fam, r in s["results"].items():
            row = {"scenario": scen, "run": d.name, "family": fam, "reached_holdout": r["stage"] == "holdout",
                   "accepted": bool(r["accepted"])}
            if r["stage"] == "holdout":
                h = r["holdout"]
                row.update(sharpe=h["sharpe"], mdd=h["max_drawdown"], pf=h["profit_factor"], trades=h["n_trades"],
                           dsr=r["dsr"]["dsr"], dsr_strict=r["dsr"]["dsr_strict"], placebo_p=r.get("placebo", {}).get("p_value"),
                           net_return=h["net_return"])
            rows.append(row)
    df = pd.DataFrame(rows)
    agg = df.groupby("scenario").agg(runs=("run", "nunique"), family_tests=("family", "size"),
                                     passed_research_gates=("reached_holdout", "sum"), accepted=("accepted", "sum")).reset_index()
    agg["gate_pass_rate"] = agg["passed_research_gates"] / agg["family_tests"]
    agg["accept_rate"] = agg["accepted"] / agg["family_tests"]
    by_fam = df.groupby(["scenario", "family"]).agg(tests=("run", "size"), reached_holdout=("reached_holdout", "sum"),
                                                    accepted=("accepted", "sum"),
                                                    median_holdout_sharpe=("sharpe", "median")).reset_index()
    ho = df[df["reached_holdout"]].drop(columns=["reached_holdout"])
    text = ["# Synthetic pipeline-validation summary\n",
            "All data here is **synthetic**. A *null* market is an exact martingale (no edge exists); *planted* markets contain "
            "an Ornstein-Uhlenbeck drift (`weak` = 0.06, `moderate` = 0.12 × base vol per hour). Purpose: measure the false-positive "
            "rate and the power of the *pipeline*, not the profitability of anything.\n",
            "## Per scenario\n", md_table(agg), "## Per scenario and family\n", md_table(by_fam),
            "## Every hold-out evaluation\n", md_table(ho.sort_values(["scenario", "run", "family"]))]
    out = root / "SUMMARY.md"
    out.write_text("\n".join(text))
    return out


if __name__ == "__main__":
    print(build())
