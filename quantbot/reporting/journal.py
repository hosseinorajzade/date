"""Append-only research journal."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def append(path: str | Path, title: str, body: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")
    with open(p, "a") as fh:
        fh.write(f"\n\n### {title}\n*{stamp}*\n\n{body.strip()}\n")
