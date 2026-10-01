"""Acceptance evaluation: every criterion from the task statement, on out-of-sample data after costs."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class Criterion:
    name: str
    value: float
    threshold: str
    passed: bool
    detail: str = ""


@dataclass
class AcceptanceReport:
    criteria: list[Criterion] = field(default_factory=list)

    @property
    def accepted(self) -> bool:
        return bool(self.criteria) and all(c.passed for c in self.criteria)

    def as_rows(self) -> list[dict]:
        return [{"criterion": c.name, "value": c.value, "threshold": c.threshold, "pass": c.passed, "detail": c.detail}
                for c in self.criteria]


def _ok(x) -> bool:
    return x is not None and not (isinstance(x, float) and np.isnan(x))


def evaluate_acceptance(acc_cfg: dict, base: dict, stressed: dict, windows_ret: list[float], dsr: dict,
                        mc: dict | None = None) -> AcceptanceReport:
    """base/stressed: dicts from runner.full_stats on the hold-out at 1.0x / stress-multiplier x costs."""
    r = AcceptanceReport()
    add = lambda *a, **k: r.criteria.append(Criterion(*a, **k))  # noqa: E731
    add("net return > 0", base["net_return"], "> 0", base["net_return"] > 0)
    add("Sharpe", base["sharpe"], f">= {acc_cfg['min_sharpe']}", _ok(base["sharpe"]) and base["sharpe"] >= acc_cfg["min_sharpe"])
    add("Sortino", base["sortino"], f">= {acc_cfg['min_sortino']}", _ok(base["sortino"]) and base["sortino"] >= acc_cfg["min_sortino"])
    add("Max drawdown", base["max_drawdown"], f"<= {acc_cfg['max_drawdown']}", base["max_drawdown"] <= acc_cfg["max_drawdown"])
    add("Profit factor", base["profit_factor"], f">= {acc_cfg['min_profit_factor']}",
        _ok(base["profit_factor"]) and base["profit_factor"] >= acc_cfg["min_profit_factor"])
    add("Trade count", base["n_trades"], f">= {acc_cfg['min_trades']}", base["n_trades"] >= acc_cfg["min_trades"])
    pos = float(np.mean(np.array(windows_ret) > 0)) if len(windows_ret) else float("nan")
    add(f"Positive {acc_cfg['window_days']}d windows", pos, f"> {acc_cfg['min_positive_window_share']}",
        _ok(pos) and pos > acc_cfg["min_positive_window_share"], f"{len(windows_ret)} windows")
    m = acc_cfg["stress_multiplier"]
    s_ok = (stressed["net_return"] > 0 and _ok(stressed["sharpe"]) and stressed["sharpe"] >= acc_cfg["min_sharpe"]
            and _ok(stressed["sortino"]) and stressed["sortino"] >= acc_cfg["min_sortino"]
            and stressed["max_drawdown"] <= acc_cfg["max_drawdown"]
            and _ok(stressed["profit_factor"]) and stressed["profit_factor"] >= acc_cfg["min_profit_factor"])
    add(f"Robust to {m}x fees+slippage", stressed["sharpe"], "Sharpe/Sortino/MDD/PF/net all still pass", bool(s_ok),
        f"stressed: net={stressed['net_return']:.3f} sharpe={stressed['sharpe']:.2f} sortino={stressed['sortino']:.2f} "
        f"mdd={stressed['max_drawdown']:.3f} pf={stressed['profit_factor']:.2f}")
    add("Deflated Sharpe", dsr["dsr"], f">= {acc_cfg['min_dsr']}", _ok(dsr["dsr"]) and dsr["dsr"] >= acc_cfg["min_dsr"],
        f"N_eff={dsr['n_effective']:.1f} (raw {dsr['n_raw']}), SR0={dsr['sr0_ann']:.2f}/yr; strict-variance DSR={dsr['dsr_strict']:.3f} "
        f"(SR0={dsr['sr0_ann_strict']:.2f}/yr)")
    return r
