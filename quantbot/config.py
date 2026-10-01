"""YAML config loading. Secrets are read from the environment (.env), never from YAML."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "config.yaml"


def load_env() -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv(ROOT / ".env")
    except ImportError:  # pragma: no cover
        pass


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    load_env()
    with open(path or DEFAULT_CONFIG) as fh:
        return yaml.safe_load(fh)


def secret(name: str, default: str | None = None) -> str | None:
    return os.environ.get(name, default)


def timeframe_to_minutes(tf: str) -> int:
    unit = tf[-1]
    n = int(tf[:-1])
    return n * {"m": 1, "h": 60, "d": 1440, "w": 10080}[unit]


def bars_per_day(tf: str) -> float:
    return 1440.0 / timeframe_to_minutes(tf)


@dataclass(frozen=True)
class Paths:
    data_dir: Path

    @property
    def raw(self) -> Path:
        return self.data_dir / "raw"

    @property
    def clean(self) -> Path:
        return self.data_dir / "clean"
