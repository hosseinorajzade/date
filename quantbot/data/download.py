"""Historical data download via ccxt (OHLCV + perpetual funding history).

Run:  python -m quantbot.data.download [--config config/config.yaml] [--symbols BTC/USDT:USDT ...]

Network note: requires outbound access to the exchange REST API. Raw pages are
appended to parquet files in data/raw/ and the download is resumable.
"""
from __future__ import annotations

import argparse
import logging
import time
from pathlib import Path

import pandas as pd

from ..config import Paths, load_config, timeframe_to_minutes

log = logging.getLogger(__name__)
OHLCV_COLS = ["open", "high", "low", "close", "volume"]


def safe_name(symbol: str) -> str:
    return symbol.replace("/", "-").replace(":", "_")


def raw_path(paths: Paths, exchange: str, symbol: str, timeframe: str, kind: str = "ohlcv") -> Path:
    return paths.raw / f"{exchange}_{safe_name(symbol)}_{timeframe if kind == 'ohlcv' else kind}.parquet"


def _retry(fn, *args, retries: int = 6, base_sleep: float = 2.0, **kwargs):
    for attempt in range(retries):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:  # network/rate-limit errors are all retried with backoff
            wait = base_sleep * (2**attempt)
            log.warning("request failed (%s); retry %d/%d in %.0fs", exc, attempt + 1, retries, wait)
            time.sleep(wait)
    raise RuntimeError(f"giving up after {retries} retries")


def fetch_ohlcv(exchange, symbol: str, timeframe: str, since_ms: int, until_ms: int | None = None,
                limit: int = 1000) -> pd.DataFrame:
    """Paginated OHLCV download. Only CLOSED bars are returned (the last, still-forming bar is dropped)."""
    tf_ms = timeframe_to_minutes(timeframe) * 60_000
    rows: list[list[float]] = []
    cursor = since_ms
    now_ms = int(exchange.milliseconds())
    until_ms = min(until_ms or now_ms, now_ms)
    while cursor < until_ms:
        page = _retry(exchange.fetch_ohlcv, symbol, timeframe, since=cursor, limit=limit)
        if not page:
            break
        rows.extend(page)
        last = page[-1][0]
        if last + tf_ms <= cursor:  # no progress
            break
        cursor = last + tf_ms
        if len(rows) % 50_000 < limit:
            log.info("%s %s: %d rows, at %s", symbol, timeframe, len(rows), pd.to_datetime(last, unit="ms", utc=True))
    df = pd.DataFrame(rows, columns=["ts"] + OHLCV_COLS)
    if df.empty:
        return df
    df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    df = df.drop_duplicates("ts", keep="last").set_index("ts").sort_index()
    df.index.name = "ts"
    # drop bars that were not closed at download time
    df = df[df.index + pd.Timedelta(milliseconds=tf_ms) <= pd.to_datetime(now_ms, unit="ms", utc=True)]
    return df


def fetch_funding(exchange, symbol: str, since_ms: int, until_ms: int | None = None) -> pd.DataFrame:
    """Funding-rate history for a perpetual (rate per funding interval, usually 8h)."""
    rows = []
    cursor = since_ms
    now_ms = int(exchange.milliseconds())
    until_ms = min(until_ms or now_ms, now_ms)
    while cursor < until_ms:
        page = _retry(exchange.fetch_funding_rate_history, symbol, since=cursor, limit=1000)
        if not page:
            break
        rows.extend((p["timestamp"], p["fundingRate"]) for p in page)
        nxt = page[-1]["timestamp"] + 1
        if nxt <= cursor:
            break
        cursor = nxt
    df = pd.DataFrame(rows, columns=["ts", "rate"])
    if df.empty:
        return df
    df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    return df.drop_duplicates("ts").set_index("ts").sort_index()


def download_symbol(cfg: dict, symbol: str, exchange=None) -> None:
    import ccxt

    m = cfg["market"]
    paths = Paths(Path(m["data_dir"]))
    paths.raw.mkdir(parents=True, exist_ok=True)
    ex = exchange or getattr(ccxt, m["exchange"])({"enableRateLimit": True})
    tf = m["timeframe"]
    path = raw_path(paths, m["exchange"], symbol, tf)
    since = int(pd.Timestamp(m["start"], tz="UTC").timestamp() * 1000)
    old = pd.read_parquet(path) if path.exists() else None
    if old is not None and len(old):
        since = int(old.index[-1].timestamp() * 1000) + 1  # resume
    df = fetch_ohlcv(ex, symbol, tf, since, int(pd.Timestamp(m["end"], tz="UTC").timestamp() * 1000) if m.get("end") else None)
    if old is not None and len(old):
        df = pd.concat([old, df]).loc[lambda d: ~d.index.duplicated(keep="last")].sort_index()
    df.to_parquet(path)
    log.info("saved %s (%d rows) -> %s", symbol, len(df), path)
    try:
        fund = fetch_funding(ex, symbol, since if old is None else int(pd.Timestamp(m["start"], tz="UTC").timestamp() * 1000))
        if len(fund):
            fund.to_parquet(raw_path(paths, m["exchange"], symbol, tf, kind="funding"))
    except Exception as exc:  # funding history is optional; engine falls back to the constant assumption
        log.warning("funding history unavailable for %s: %s", symbol, exc)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=None)
    ap.add_argument("--symbols", nargs="*", default=None)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    cfg = load_config(args.config)
    for sym in args.symbols or cfg["market"]["universe"]:
        download_symbol(cfg, sym)


if __name__ == "__main__":
    main()
