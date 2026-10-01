# quantbot — systematic crypto trading research, backtest and paper-trading framework

> ## Honest status (read this first)
>
> **No strategy has been validated on real market data, and none is claimed to have an edge.**
> The development sandbox this was built in blocks every exchange / market-data host (HTTP 403 from the egress
> proxy: `api.binance.com`, `data-api.binance.vision`, `data.binance.vision`, `api.bybit.com`, `www.okx.com`,
> `api.kraken.com`, `api.exchange.coinbase.com`, `query1.finance.yahoo.com`). Only PyPI was reachable. I did **not**
> work around the policy and I did **not** substitute fabricated data for real data.
>
> What *was* built and verified: the complete research / validation / paper-trading framework, validated for
> **correctness and statistical honesty on synthetic markets** (a market with a known absence of edge and markets with
> a planted edge). Those synthetic runs test the *machinery*; they are **not** evidence about BTC.
> The acceptance criteria are therefore **unmet / untested on real data**. One command runs the full real-data
> research once the data host is reachable (see "Running the real research").

## Assumptions (task placeholders → pre-registered defaults, `config/config.yaml`)

| Placeholder | Value used |
|---|---|
| MARKET | Binance USDT-M perpetual futures, primary **BTC/USDT**; ETH, BNB, XRP, LTC, ADA as cross-asset checks (parameters are chosen on BTC only and never re-fit) |
| TIMEFRAME | 1h |
| X % risk per trade | 1% of equity to the stop (+ 2× gross leverage cap, 3% daily loss limit, 15% drawdown kill switch) |
| N weeks paper | 4 weeks minimum before live is permitted |
| Costs | 5 bps taker fee + 3 bps slippage per side (+3 bps extra on stop fills), funding 1 bp / 8h fallback (real history used when downloaded) |
| Splits | train ≤ 2022-12-31, validation ≤ 2024-06-30, **hold-out afterwards (one look per strategy family)** |

Change them *before* running research, never after looking at results.

## Layout

```
config/config.yaml        all assumptions, costs, risk limits, gates, acceptance thresholds
quantbot/
  data/        download (ccxt, resumable), clean (gaps/outliers/dupes/UTC), splits + HoldoutVault, synthetic markets
  strategies/  4 pre-registered families, causal features, look-ahead audit
  risk/        fixed-fractional / vol-scaled position sizing (single numba function shared by backtest+paper+live)
  backtest/    numba bar engine, costs, metrics, walk-forward, validation (sensitivity, cost stress, regimes, placebo),
               stats (PSR, deflated Sharpe, bootstraps, MC), trial registry, acceptance evaluator
  execution/   paper trader, state store, Telegram alerts, ccxt client w/ retry+reconnect, live gate, live trader
  research/    pipeline.py (end-to-end), synthetic_validation.py
  reporting/   plots, markdown reports, journal
reports/       journal.md (every iteration), synthetic/ (pipeline-validation runs), holdout_log.json
tests/         70 tests (engine accounting, look-ahead audits, stats calibration, replay parity, gate, reconnect…)
```

## Setup

```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # only needed for authenticated exchange access / Telegram; never commit .env
pytest                      # whole suite (a few tests are marked slow; all run by default)
```

## Running the real research (needs outbound access to the exchange API)

```bash
python -m quantbot.data.download                 # BTC + universe, 1h bars + funding history -> data/raw/*.parquet
python -m quantbot.research.run_real --out reports/real_run_1   # research -> single hold-out look -> report.md + journal
```

Do **not** inspect hold-out data by hand before this runs. `HoldoutVault` records every hold-out access in
`holdout_log.json` and refuses a second look for the same strategy family. A new idea = a new family (and a larger
trial count in the deflation).

## Research protocol (what the pipeline enforces)

1. **Data** — `clean_ohlcv`: UTC grid, dedupe, bad-tick (spike-and-revert) removal that *keeps* genuine crashes, short
   gaps flat-filled and flagged, long gaps left invalid (no signal, no trading). No splits/dividends in crypto;
   survivorship bias is acknowledged below.
2. **Hypotheses (pre-registered, small grids)** — `donchian` (time-series momentum), `meanrev` (liquidity-shock reversion
   in choppy regimes), `squeeze` (volatility compression → expansion), `ml_gbm` (regularised walk-forward gradient boosting).
   Each has an economic rationale in its module docstring. 80 configurations in total; **every one counts as a trial**.
3. **Realistic engine** — decision at bar-t close, fill at bar-(t+1) open ± slippage, fees, funding, intrabar stops
   (gap-through fills at the open, stop-market extra slippage), 1% risk sizing, exposure cap, daily loss limit, kill switch.
4. **Validation** — stage 1 on train+validation only: look-ahead audit → all configs → rolling walk-forward (365d train /
   90d test, plateau-smoothed selection) → parameter-neighbour sensitivity → *gates*. Only families that pass reach the
   hold-out (stage 2, **one look**): frozen params, cost stress, Monte Carlo, bootstrap, regimes, other assets,
   time-shift placebo, deflated Sharpe with the *complete* trial registry.
5. **Acceptance (all must hold on the hold-out, after costs)** — net>0, Sharpe≥1.0, Sortino≥1.5, MDD≤20%, PF≥1.3,
   ≥200 trades, >50% of 90-day windows positive, all of {net>0, Sharpe, Sortino, MDD, PF} still pass at 1.5× fees+slippage,
   deflated Sharpe ≥ 0.95.

### Interpretation choices (stated so they cannot be changed silently)
* "Robust to +50% fees/slippage" = *every* headline criterion (Sharpe, Sortino, MDD, PF, net>0) still passes at 1.5×.
* Deflated Sharpe (Bailey & López de Prado 2014): N = participation ratio of the trial-return correlation spectrum
  (not the raw count); benchmark variance = **null sampling variance 1/(T−1)**. The *strict* variant (empirical
  cross-trial variance, raw N) is always reported alongside. Reason for the primary choice: the empirical variance mixes
  genuine between-strategy differences into the null spread and, in my planted-edge tests, inflated the benchmark to a
  Sharpe of ~3.2 so that *no* strategy could ever pass. See `reports/journal.md` (iteration 0.3).
* If several families are accepted, pick by *research* walk-forward performance, never by hold-out ranking.

## Integrity mechanisms (all tested)
* Look-ahead: truncation-invariance audit on every family + canary strategies (shift(-1), full-sample z-score,
  centred window) that the audit **must** flag; engine test that wrecking future bars cannot change past equity; ML
  scores are provably unchanged when future prices are scrambled.
* Engine bias: on a martingale price path, random entries must have mean R = 0 (statistical test over >1000 trades, both
  trailing modes). This test caught a real artefact (see journal).
* Deflated-Sharpe calibration: best of 60 zero-skill strategies passes an undeflated test 96% of the time and the
  deflated test 0% of the time.
* Hold-out vault, trial registry, time-shift placebo, ledger reconciliation in paper trading.

## Paper trading → live

```bash
# set paper.strategy / paper.params in config.yaml ONLY after a strategy passed the hold-out
python -m quantbot.execution.run --mode paper     # PaperTrader on closed bars, state in paper_state/
python -m quantbot.execution.run --mode gate      # shows which live-gate conditions are met
```
* `PaperTrader` calls the **same compiled `step()` kernel** as the backtest; replaying history through it reproduces the
  backtest equity and trades to 1e-10 (tested). Atomic state file, idempotent re-delivery, gap detection, restart resume,
  ledger-vs-engine reconciliation after every bar (mismatch ⇒ halt + critical alert), stale-feed / kill-switch /
  daily-limit alerts, Telegram via `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` from the environment.
* Live is refused unless **all** hold: `live.enabled: true`, env `LIVE_TRADING_CONFIRM=YES`, and the paper gate (≥4 weeks,
  ≥95% bar coverage, ≥20 trades, non-negative net return, drawdown ≤20%, zero unreconciled errors, unchanged strategy).
  `LiveTrader` cannot even be constructed otherwise. **The live order path has only been tested against a fake exchange.**
  Validate on the exchange testnet (`live.sandbox: true`) before real money; the CLI intentionally does not wire up the
  live loop.

## Limitations and risks
* **No real-data evidence yet** (see top). All performance claims in `reports/synthetic/` are about the machinery.
* Survivorship: the universe is the coins that still exist; delisted coins are invisible to exchange APIs.
* Funding is spread uniformly across bars; real funding is charged at 00/08/16 UTC. Real funding history is used if downloaded.
* Fills assume liquidity at the next open ± fixed bps; no queue/partial-fill/market-impact model (fine for retail size on BTC, not for size).
* Daily-bar risk limits are evaluated at bar close and acted on at the next open (intrabar breaches are not caught except via stops).
* A paper trader recomputes signals on a trailing window; state-machine strategies can differ from the backtest for the first
  trade after a cold start (the replay-parity test uses the full history).
* Crypto regimes are few; a 2–3 year hold-out contains few independent market regimes, whatever the trade count.
* 1h strategies pay ~16 bps per round trip; edges smaller than that vanish. This is the most likely reason a real run fails.
