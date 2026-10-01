"""Alerting. Telegram credentials come from the environment (.env), never from YAML or source."""
from __future__ import annotations

import logging
import time

import requests

from ..config import secret

log = logging.getLogger("alerts")


class Alerter:
    """Base alerter: logs and records only. Alert failures must never break trading."""

    def __init__(self, min_interval_s: float = 1.0):
        self.min_interval_s = min_interval_s
        self._last: dict[str, float] = {}
        self.sent: list[tuple[str, str]] = []

    def send(self, message: str, level: str = "info", dedupe_key: str | None = None) -> bool:
        key = dedupe_key or message
        now = time.monotonic()
        if level != "critical" and now - self._last.get(key, -1e9) < self.min_interval_s:
            return False
        self._last[key] = now
        self.sent.append((level, message))
        getattr(log, "error" if level in ("error", "critical") else "info")("[ALERT %s] %s", level, message)
        try:
            self._deliver(f"[{level.upper()}] {message}")
        except Exception as exc:  # noqa: BLE001
            log.warning("alert delivery failed: %s", exc)
            return False
        return True

    def _deliver(self, text: str) -> None:  # overridden by concrete alerters
        pass


class TelegramAlerter(Alerter):
    def __init__(self, token: str | None = None, chat_id: str | None = None, **kw):
        super().__init__(**kw)
        self.token = token or secret("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or secret("TELEGRAM_CHAT_ID")
        if not (self.token and self.chat_id):
            raise ValueError("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set")

    def _deliver(self, text: str) -> None:
        r = requests.post(f"https://api.telegram.org/bot{self.token}/sendMessage",
                          json={"chat_id": self.chat_id, "text": text[:4000]}, timeout=10)
        r.raise_for_status()


def build_alerter(cfg: dict) -> Alerter:
    if cfg.get("telegram", {}).get("enabled"):
        try:
            return TelegramAlerter(min_interval_s=30.0)
        except ValueError as exc:
            log.warning("telegram disabled: %s", exc)
    return Alerter()
