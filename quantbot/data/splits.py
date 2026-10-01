"""Chronological train / validation / hold-out split and the hold-out vault.

The hold-out is only reachable through HoldoutVault.open(family, ...), which records every access
in reports/holdout_log.json and refuses a second look for the same strategy family. This is a
procedural guard against hold-out peeking, not a cryptographic one: it makes accidental reuse loud.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


class HoldoutAlreadyUsed(RuntimeError):
    pass


@dataclass(frozen=True)
class DataSplit:
    train_end: pd.Timestamp
    val_end: pd.Timestamp

    @classmethod
    def from_config(cls, cfg: dict) -> "DataSplit":
        s = cfg["splits"]
        return cls(pd.Timestamp(s["train_end"], tz="UTC") + pd.Timedelta(days=1),
                   pd.Timestamp(s["val_end"], tz="UTC") + pd.Timedelta(days=1))

    def train(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[df.index < self.train_end]

    def validation(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[(df.index >= self.train_end) & (df.index < self.val_end)]

    def research(self, df: pd.DataFrame) -> pd.DataFrame:
        """Everything the researcher may look at while developing (train + validation)."""
        return df[df.index < self.val_end]

    def _holdout(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[df.index >= self.val_end]


class HoldoutVault:
    def __init__(self, split: DataSplit, log_path: str | Path = "reports/holdout_log.json"):
        self.split = split
        self.log_path = Path(log_path)

    def _read(self) -> list[dict]:
        if self.log_path.exists():
            return json.loads(self.log_path.read_text())
        return []

    def used_by(self, family: str) -> list[dict]:
        return [e for e in self._read() if e["family"] == family]

    def open(self, df: pd.DataFrame, family: str, params: dict, allow_retouch: bool = False) -> pd.DataFrame:
        """Return the hold-out slice and log the access. One look per strategy family."""
        prior = self.used_by(family)
        if prior and not allow_retouch:
            raise HoldoutAlreadyUsed(
                f"hold-out already evaluated for family '{family}' on {prior[0]['when']}. "
                "A second look invalidates it as out-of-sample data. Define a new family instead."
            )
        ho = self.split._holdout(df)
        entry = {
            "family": family,
            "params": params,
            "when": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "rows": int(len(ho)),
            "first": str(ho.index[0]) if len(ho) else None,
            "last": str(ho.index[-1]) if len(ho) else None,
            "data_hash": hashlib.sha256(ho["close"].to_numpy().tobytes()).hexdigest()[:16] if len(ho) else None,
            "retouch": bool(prior),
        }
        log = self._read() + [entry]
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.write_text(json.dumps(log, indent=2, default=str))
        return ho
