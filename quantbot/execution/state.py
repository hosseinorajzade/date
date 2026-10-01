"""Crash-safe persisted trader state (atomic JSON writes) and append-only CSV ledgers."""
from __future__ import annotations

import csv
import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np


@dataclass
class TraderState:
    S: list[float]
    i: int = 0
    pending_tgt: float = 0.0
    pending_sd: float = float("nan")
    last_bar: str | None = None
    first_bar: str | None = None
    bars_processed: int = 0
    n_trades: int = 0
    initial_equity: float = 1.0
    unreconciled_errors: int = 0
    halted: bool = False
    halt_reason: str = ""
    entry_ts: str | None = None
    realized_net: float = 0.0
    strategy: dict = field(default_factory=dict)

    @property
    def S_arr(self) -> np.ndarray:
        return np.asarray(self.S, dtype=float)


def _enc(x: float):
    return "NaN" if isinstance(x, float) and np.isnan(x) else x


def _dec(x) -> float:
    return float("nan") if x == "NaN" else float(x)


class StateStore:
    def __init__(self, directory: str | Path):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.state_path = self.dir / "state.json"
        self.trades_path = self.dir / "trades.csv"
        self.equity_path = self.dir / "equity.csv"
        self.events_path = self.dir / "events.log"

    def load(self) -> TraderState | None:
        if not self.state_path.exists():
            return None
        d = json.loads(self.state_path.read_text())
        d["S"] = [_dec(x) for x in d["S"]]
        d["pending_sd"] = _dec(d["pending_sd"])
        d["pending_tgt"] = _dec(d["pending_tgt"])
        return TraderState(**d)

    def save(self, st: TraderState) -> None:
        d = asdict(st)
        d["S"] = [_enc(float(x)) for x in d["S"]]
        d["pending_sd"] = _enc(float(d["pending_sd"]))
        d["pending_tgt"] = _enc(float(d["pending_tgt"]))
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(d, indent=1))
        os.replace(tmp, self.state_path)  # atomic on POSIX: never a half-written state file

    def _append(self, path: Path, header: list[str], row: list) -> None:
        new = not path.exists()
        with open(path, "a", newline="") as fh:
            w = csv.writer(fh)
            if new:
                w.writerow(header)
            w.writerow(row)

    def log_trade(self, row: list) -> None:
        self._append(self.trades_path, ["entry_time", "exit_time", "side", "units", "entry_px", "exit_px", "gross",
                                        "fees", "funding", "net", "reason", "risk"], row)

    def log_equity(self, ts, equity: float, units: float, price: float) -> None:
        self._append(self.equity_path, ["ts", "equity", "units", "price"], [ts, equity, units, price])

    def event(self, text: str) -> None:
        with open(self.events_path, "a") as fh:
            fh.write(f"{text}\n")
