"""Registry of EVERY strategy variant evaluated on research data (the denominator of the multiple-testing problem).

Each (family, params) config that is backtested for selection purposes is recorded with its research-period
daily returns. The deflated Sharpe ratio is computed from this registry, so the count cannot be quietly reduced.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import stats


def config_key(family: str, params: dict) -> str:
    return family + "|" + ",".join(f"{k}={params[k]}" for k in sorted(params))


class TrialRegistry:
    def __init__(self, directory: str | Path):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.meta_path = self.dir / "trials.jsonl"
        self.ret_path = self.dir / "trial_returns.parquet"
        self._meta: dict[str, dict] = {}
        if self.meta_path.exists():
            for line in self.meta_path.read_text().splitlines():
                if line.strip():
                    d = json.loads(line)
                    self._meta[d["key"]] = d
        self._rets = pd.read_parquet(self.ret_path) if self.ret_path.exists() else pd.DataFrame()

    def record(self, family: str, params: dict, daily_ret: pd.Series, note: str = "") -> None:
        key = config_key(family, params)
        sr = stats.moments(daily_ret.to_numpy())[0]
        self._meta[key] = {"key": key, "family": family, "params": params, "sr_daily": None if np.isnan(sr) else float(sr),
                           "n_days": int(len(daily_ret)), "note": note}
        self._rets = self._rets.reindex(self._rets.index.union(daily_ret.index))
        self._rets[key] = daily_ret

    def flush(self) -> None:
        self.meta_path.write_text("\n".join(json.dumps(v) for v in self._meta.values()) + "\n")
        self._rets.to_parquet(self.ret_path)

    @property
    def n_trials(self) -> int:
        return len(self._meta)

    def families(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for m in self._meta.values():
            out[m["family"]] = out.get(m["family"], 0) + 1
        return out

    def trial_sharpes(self) -> np.ndarray:
        return np.array([m["sr_daily"] for m in self._meta.values() if m["sr_daily"] is not None])

    def deflation_inputs(self) -> dict:
        """Inputs for the deflated Sharpe ratio.

        * n_trials_raw        : every config ever evaluated on research data (never reduced by hand)
        * n_trials_effective  : participation ratio of the trials' return-correlation spectrum
        * trial_sr_var_null   : sampling variance of a zero-skill Sharpe estimate, 1/(T-1)  [PRIMARY]
        * trial_sr_var_daily  : empirical cross-trial variance of the Sharpes [STRICT sensitivity: it mixes true
                                differences between strategies into the null spread and so over-penalises]
        """
        srs = self.trial_sharpes()
        var_emp = float(np.var(srs, ddof=1)) if len(srs) > 1 else 0.0
        mat = self._rets.fillna(0.0).to_numpy() if len(self._rets) else np.zeros((0, 0))
        n_eff = stats.effective_n_trials(mat) if mat.shape[1] > 1 else float(self.n_trials)
        t_obs = int(np.median([m["n_days"] for m in self._meta.values()])) if self._meta else 0
        return {"n_trials_raw": self.n_trials, "n_trials_effective": float(n_eff), "trial_sr_var_daily": var_emp,
                "trial_sr_var_null": stats.null_sharpe_variance(t_obs), "n_days_research": t_obs,
                "by_family": self.families()}
