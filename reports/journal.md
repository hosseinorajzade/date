# Research journal

Chronological, append-only in spirit. Every iteration is logged, including the failures and the mistakes in my own
tooling. Auto-generated per-run entries (family-level gate verdicts / hold-out results) are written to
`<run dir>/journal.md` by the pipeline; synthetic ones live under `reports/synthetic/*/journal.md`.
**Nothing in this file is a result on real market data** — see iteration 0.1.

---

## Iteration 0 — Pre-registration (written before any data of any kind was looked at)

*Assumptions* (task placeholders filled with defaults; see `config/config.yaml`): Binance USDT-M perpetuals, BTC/USDT
primary (ETH/BNB/XRP/LTC/ADA cross-checks, no re-fitting), 1h bars, 1% equity risk per trade, 4 weeks of paper trading
before live. Costs: 5 bps fee + 3 bps slippage per side (+3 bps on stop fills), 1 bp/8h funding fallback.
Chronological split: train ≤ 2022-12-31, validation ≤ 2024-06-30, hold-out afterwards, one look per family.

*Hypotheses (4 families, 80 configurations, all counted as trials):*
1. `donchian` — time-series momentum (24 configs): crypto trends persist at multi-day horizons.
2. `meanrev` — liquidity-shock reversion gated by low efficiency ratio (36 configs).
3. `squeeze` — volatility compression → expansion breakout with trailing stop (12 configs).
4. `ml_gbm` — walk-forward regularised gradient boosting, min-hold = horizon (8 configs). Included mostly as the best
   stress test of the multiple-testing machinery (highest overfit risk).

*Prior beliefs (so they can be checked later):* on a 1h grid with ~16 bps round-trip cost I expect `meanrev` and
`squeeze` to fail, `ml_gbm` to fail, and `donchian` with long lookbacks to be the only plausible survivor — and even it
may fail the ≥200-trades criterion (slow trend systems trade rarely).

*Gates to reach the hold-out:* WFO OOS Sharpe ≥ 0.8, ≥50% of WFO windows positive, ≥100 research trades, ≥60% of
one-step-neighbour configs with Sharpe > 0. *Acceptance:* exactly the task's list (see README for the interpretation of
"robust to +50% costs" and of the deflated Sharpe).

---

## Iteration 0.1 — Environment blocks all market-data access (2026-10-01)

Outbound HTTPS from the sandbox is policy-filtered. `curl` to `api.binance.com`, `data-api.binance.vision`,
`data.binance.vision`, `api.bybit.com`, `www.okx.com`, `api.kraken.com`, `api.exchange.coinbase.com` and
`query1.finance.yahoo.com` all returned **403 from the egress proxy** (`CONNECT tunnel failed`); `pypi.org` returned 200.
The proxy status endpoint records these as `connect_rejected` policy denials.

**Decision:** do not route around the policy and do not substitute made-up data for real data. Build everything that
does not depend on the data, validate the machinery on synthetic markets (clearly labelled), and make the real run a
single command (`python -m quantbot.research.run_real`). Consequence: **the acceptance criteria cannot be evaluated;
no strategy is claimed to have an edge.**

To unblock: add (at least) `data-api.binance.vision` / `fapi.binance.com` (or `api.bybit.com` / `www.okx.com` and
change `market.exchange`) to the environment's allowed domains (Network access setting), then run the download + research
commands in the README.

---

## Iteration 0.2 — A flaw in my own synthetic generator produced a fake edge (caught by placebo tests)

*What happened.* First synthetic validation (generator v1: per-bar return drawn first, intrabar path interpolated to it
with 12 sub-steps) on 6 **null** markets: nothing was fully accepted, but the `squeeze` family **passed the research gates
in 4 of 6 null seeds** (seeds 0, 1, 3, 5) and posted hold-out Sharpe +1.69, +1.66, +0.96, +0.94 (net of costs, PF up to
1.51); `ml_gbm` also passed once (seed 1, hold-out Sharpe +0.95). That is far above any plausible false-positive rate for a
market with no edge, so I treated it as a bug until proven otherwise.

*Diagnosis (zero costs, 12–16 null seeds, mean Sharpe ± s.e.):*

| test | v1 generator (12 substeps) |
|---|---|
| squeeze strategy | +0.46 … +0.88 |
| squeeze, signal **reversed** | +0.09 … +0.67 |
| squeeze, signal **time-shifted** (placebo) | +0.52 … +0.79 (4σ) |
| **random** entries + trailing stop | +0.33 … +0.57 |

Reversing or shifting the signal changed nothing ⇒ the "edge" did not come from the signal. Two defects found:
(a) v1 drew the bar return first and bridged the intrabar path toward it with an under-scaled bridge, so intrabar
increments were positively autocorrelated and stops looked profitable; (b) with only 12 sub-steps, price overshoots a stop level
before the next sub-step, while the engine (correctly, for a continuous market) fills at the stop — a direction-independent
gift of about one sub-step per stop-out. Fix: iid Gaussian increments, 120 sub-steps/bar, martingale-corrected (zero
*arithmetic* drift; zero *log* drift would give longs a free σ²/2 per year).

*After the fix* (120 sub-steps, 40 seeds × 2 y, ~2,600 random trades per mode, zero cost): mean R per trade
**−0.002 ± 0.026** (fixed stop) and **+0.014 ± 0.020** (trailing), long and short balanced — i.e. the engine is unbiased.
With 12 sub-steps the trailing case read +0.033 ± 0.021. Squeeze on the fixed generator: −0.02 ± 0.16 (placebo +0.04 ± 0.12).

*Permanent safeguards added:* `test_engine_is_unbiased_on_a_martingale_…` (mean R must be ~0 for random entries on a
martingale), `test_null_market_is_a_martingale_…`, and a **time-shift placebo test** inside the hold-out stage of the real
pipeline (the real run will report the placebo p-value for every candidate). All v1 synthetic outputs were discarded.
*Lesson for the real run:* an unexpected edge in a simulation or a backtest is a bug until a placebo says otherwise.

---

## Iteration 0.3 — Deflated-Sharpe benchmark was mis-specified (found via the planted-edge power test)

*What happened.* On planted-trend markets Donchian reached hold-out Sharpe ≈ 1.5 with a genuinely harvestable edge (placebo
p ≈ 0.01–0.08) yet DSR ≈ 0.01, so nothing could ever be accepted. Cause: the expected-maximum-Sharpe benchmark
SR0 = √V · E[max of N std-normals] used **V = the empirical cross-trial variance of Sharpes**. My 80-config pool contains
structurally good strategies (Donchian trial Sharpes averaged +1.6/yr) and structurally bad ones (mean reversion averaged
−1.2/yr, pure cost drag), so empirical std = 1.31/yr versus 0.46/yr of pure estimation noise for a 4.7-year sample; SR0
came out at **3.2/yr**. The formula assumes trials are draws from the null; a heterogeneous pool violates that and makes
the test unpassable for any Sharpe below ~3 regardless of how real the edge is.
Also N_eff by "average correlation" gave 74 of 80 for clearly clustered configs.

*Change (decided on synthetic data, before any real data exists):*
1. Primary DSR uses the **null sampling variance 1/(T−1)** of a zero-skill Sharpe estimate.
2. N_eff = **participation ratio** of the trial-correlation spectrum (74 → ≈ 8 here: the four families are the real
   independent degrees of freedom).
3. The strict variant (empirical variance, raw N) stays in every report as a sensitivity (it is ~0.00 everywhere).
4. Calibration test: the best of 60 zero-skill strategies passes an undeflated PSR>0.95 test 96% of the time and the
   deflated test 0.0% of the time (nominal 5%).

This is a loosening relative to my first implementation, made for a stated statistical reason and disclosed here, in the
README and in every report. It does **not** touch the 0.95 threshold or any other criterion.

---

## Iteration 0.4 — Final synthetic pipeline validation (corrected generator + corrected DSR)

Scenarios fixed in advance of looking at results: `null` (12 seeds), `planted_weak` (OU drift strength 0.06, 4 seeds),
`planted_moderate` (0.12, 4 seeds; added after measuring that the corrected generator makes 0.06 a *very* weak edge:
daily autocorrelation 0.046 vs −0.013 for null). 7 years of hourly bars each, same splits as the real config.
Full table: `reports/synthetic/SUMMARY.md`; sample reports in `reports/synthetic/{null,planted_weak,planted_moderate}_seed0/report.md`.

| scenario | family-tests | passed research gates | **accepted** |
|---|---|---|---|
| null (no edge exists) | 48 | **0** | **0** |
| planted weak | 16 | 9 | **0** |
| planted moderate | 16 | 12 | **9** |

Findings (about the *pipeline*):
* **False positives:** 0/48 gate passes on markets with no edge (95% upper bound ≈ 6%); the hold-out was never opened for them.
* **Power:** with a moderate planted edge 9 of 12 hold-out evaluations are accepted (the rest fail on one criterion: trade
  count, drawdown or the 1.5× cost stress). With a weak edge the genuine winners (Donchian, hold-out Sharpe ≈ 1.5, DSR
  0.88–0.92, placebo p 0.02–0.08) are correctly **not** accepted: the evidence is real but not strong enough, and they trade
  only 70–140 times in the hold-out. A realistic crypto edge looks more like the weak case than the moderate one, so
  **the acceptance bar is demanding**: expect to need a hold-out Sharpe of roughly 1.9–2.0 (DSR ≥ 0.95 given ≈ 8 effective
  trials, SR0 ≈ 0.67/yr, over a ~2.2-year hold-out whose Sharpe has a standard error of ≈ 0.7) in addition to the 200-trade requirement.
* Slow trend systems are limited by the ≥200-trades criterion on a ~2.2-year hold-out: Donchian trades ≈ 28/yr at n=192, 50/yr at n=96, 91/yr at n=48, 163/yr at n=24 (measured on research spans), so n ≥ 96 cannot reach 200 trades; the weak-edge winners chose n=96–192.
* The walk-forward windows, sensitivity tables, cost stress, MC/bootstrap, regime and cross-asset blocks all populate.

Limits of this evidence: one synthetic data-generating process, 4–12 seeds per scenario, planted edge of the type the
`donchian` family is built to catch (so power for *other* kinds of edge is untested).

---

## Iteration 1 — Real-data research: NOT RUN (blocked by Iteration 0.1)

Nothing to report. When data access is available the order of operations is fixed:
1. `python -m quantbot.data.download` (inspect the cleaning report: gaps, bad ticks, longest gap).
2. `python -m quantbot.research.run_real --out reports/real_run_1` — stage 1 on train+validation for all four families
   (80 trials), then at most one hold-out look per family that passed the gates.
3. Whatever comes out is logged here, including a total failure. **If no family is accepted the correct conclusion is
   "no tradable edge found at this cost level" — not looser thresholds.** New ideas become *new families*, which enlarge
   the trial count used by the deflated Sharpe and cannot reuse a burned hold-out.
4. Only an accepted family may be written into `paper.strategy`; paper trading for ≥ 4 weeks and `--mode gate` must pass
   before the live gate opens, and live must first be exercised on exchange testnet.
