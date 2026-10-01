"""ccxt exchange wrapper with retry/backoff and automatic reconnect.

NOT exercised against a real exchange in this build (the development sandbox had no market-data network
access). Read-only market-data calls are simple and standard; order placement (`market_order`, `stop_order`)
must be validated on the exchange TESTNET before any live use.
"""
from __future__ import annotations

import logging
import time

import pandas as pd

from ..config import secret, timeframe_to_minutes

log = logging.getLogger("exchange")


class ExchangeClient:
    def __init__(self, exchange_id: str, symbol: str, timeframe: str, sandbox: bool = True,
                 max_retries: int = 6, base_sleep: float = 2.0):
        self.exchange_id, self.symbol, self.timeframe = exchange_id, symbol, timeframe
        self.sandbox, self.max_retries, self.base_sleep = sandbox, max_retries, base_sleep
        self.tf_ms = timeframe_to_minutes(timeframe) * 60_000
        self.ex = None
        self.reconnects = 0
        self._build()

    def _build(self) -> None:
        import ccxt

        params: dict = {"enableRateLimit": True, "options": {"defaultType": "future"}}
        key, sec = secret("EXCHANGE_API_KEY"), secret("EXCHANGE_API_SECRET")
        if key and sec:
            params.update(apiKey=key, secret=sec)
            if secret("EXCHANGE_PASSWORD"):
                params["password"] = secret("EXCHANGE_PASSWORD")
        self.ex = getattr(ccxt, self.exchange_id)(params)
        if self.sandbox:
            self.ex.set_sandbox_mode(True)

    def reconnect(self) -> None:
        self.reconnects += 1
        log.warning("reconnecting to %s (#%d)", self.exchange_id, self.reconnects)
        self._build()

    def _call(self, fn_name: str, *args, **kwargs):
        last = None
        for attempt in range(self.max_retries):
            try:
                return getattr(self.ex, fn_name)(*args, **kwargs)
            except Exception as exc:  # noqa: BLE001 - network, rate limit, 5xx: all retried
                last = exc
                wait = min(self.base_sleep * 2**attempt, 120)
                log.warning("%s failed (%s); retry %d/%d in %.0fs", fn_name, exc, attempt + 1, self.max_retries, wait)
                time.sleep(wait)
                if attempt >= 2:
                    self.reconnect()
        raise ConnectionError(f"{fn_name} failed after {self.max_retries} attempts: {last}")

    # ---- market data ----
    def now_ms(self) -> int:
        return int(self.ex.milliseconds())

    def fetch_closed_bars(self, since: pd.Timestamp | None = None, limit: int = 1000) -> pd.DataFrame:
        since_ms = int(since.timestamp() * 1000) if since is not None else None
        rows = self._call("fetch_ohlcv", self.symbol, self.timeframe, since=since_ms, limit=limit)
        df = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "volume"])
        if df.empty:
            return df
        df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
        df = df.drop_duplicates("ts").set_index("ts").sort_index()
        return df[df.index + pd.Timedelta(milliseconds=self.tf_ms) <= pd.to_datetime(self.now_ms(), unit="ms", utc=True)]

    def fetch_history(self, n_bars: int) -> pd.DataFrame:
        end = pd.to_datetime(self.now_ms(), unit="ms", utc=True)
        since = end - pd.Timedelta(milliseconds=self.tf_ms * (n_bars + 5))
        parts = []
        while since < end:
            page = self.fetch_closed_bars(since, 1000)
            if page.empty:
                break
            parts.append(page)
            since = page.index[-1] + pd.Timedelta(milliseconds=self.tf_ms)
        if not parts:
            return pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
        out = pd.concat(parts)
        return out[~out.index.duplicated(keep="last")].sort_index().tail(n_bars)

    # ---- account / orders (LIVE ONLY; validate on testnet first) ----
    def fetch_equity(self) -> float:
        bal = self._call("fetch_balance")
        return float(bal["total"].get("USDT", 0.0))

    def fetch_position(self) -> float:
        """Signed position in base units (long > 0)."""
        for p in self._call("fetch_positions", [self.symbol]):
            if p.get("symbol") == self.symbol:
                amt = float(p.get("contracts") or 0.0) * float(p.get("contractSize") or 1.0)
                return amt if p.get("side") == "long" else -amt
        return 0.0

    def market_order(self, side: str, amount: float, reduce_only: bool = False):
        return self._call("create_order", self.symbol, "market", side, amount, None, {"reduceOnly": reduce_only})

    def stop_order(self, side: str, amount: float, stop_price: float):
        return self._call("create_order", self.symbol, "STOP_MARKET", side, amount, None,
                          {"stopPrice": stop_price, "reduceOnly": True})

    def cancel_all(self):
        return self._call("cancel_all_orders", self.symbol)
