# SYNTHETIC planted moderate trend (seed 0) — pipeline validation

> Synthetic data. Demonstrates the pipeline's behaviour; says nothing about real markets.

Trials registered: **80** configurations (effective independent ≈ 7.8); by family: {'donchian': 24, 'meanrev': 36, 'squeeze': 12, 'ml_gbm': 8}

## Summary

| family | stage | params | net | sharpe | sortino | mdd | PF | trades | DSR | accepted |
|---|---|---|---|---|---|---|---|---|---|---|
| donchian | hold-out | {'allow_short': True, 'k_atr': 4.0, 'n': 48} | 7.275 | 5.036 | 10.102 | 0.125 | 3.222 | 224.000 | 1.000 | yes |
| meanrev | rejected at research | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | n/a | n/a | n/a | n/a | n/a | n/a | n/a | no |
| squeeze | hold-out | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 1.249 | 2.884 | 6.094 | 0.109 | 1.819 | 360.000 | 1.000 | yes |
| ml_gbm | hold-out | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | 10.772 | 4.688 | 9.454 | 0.109 | 2.694 | 317.000 | 1.000 | yes |

## Family `donchian`

### Research grid (every configuration tried; all count as trials)

| params | research_sharpe | research_ret | research_trades | train_sharpe | val_sharpe | val_ret | research_mdd |
|---|---|---|---|---|---|---|---|
| {'n': 48, 'k_atr': 4.0, 'allow_short': True} | 5.154 | 104.921 | 446 | 5.396 | 4.646 | 2.660 | 0.134 |
| {'n': 48, 'k_atr': 3.0, 'allow_short': True} | 5.091 | 287.925 | 445 | 5.275 | 4.705 | 3.802 | 0.152 |
| {'n': 24, 'k_atr': 4.0, 'allow_short': True} | 4.862 | 78.953 | 891 | 5.160 | 4.167 | 1.922 | 0.123 |
| {'n': 96, 'k_atr': 4.0, 'allow_short': True} | 4.679 | 55.906 | 238 | 4.534 | 5.044 | 2.948 | 0.136 |
| {'n': 48, 'k_atr': 2.0, 'allow_short': True} | 4.677 | 955.628 | 447 | 4.818 | 4.394 | 5.907 | 0.201 |
| {'n': 96, 'k_atr': 3.0, 'allow_short': True} | 4.586 | 122.318 | 240 | 4.388 | 5.087 | 4.203 | 0.166 |
| {'n': 192, 'k_atr': 4.0, 'allow_short': True} | 4.557 | 33.574 | 132 | 4.368 | 5.237 | 2.797 | 0.099 |
| {'n': 24, 'k_atr': 3.0, 'allow_short': True} | 4.507 | 180.815 | 891 | 4.713 | 4.033 | 2.778 | 0.145 |
| {'n': 192, 'k_atr': 2.0, 'allow_short': True} | 4.394 | 197.131 | 144 | 4.766 | 3.883 | 3.021 | 0.174 |
| {'n': 96, 'k_atr': 2.0, 'allow_short': True} | 4.367 | 333.872 | 243 | 4.671 | 3.716 | 3.230 | 0.170 |

_24 configurations in total; top 10 by research Sharpe shown. Median research Sharpe 3.79._

### Walk-forward (re-optimised each window; out-of-sample test spans)

| test_start | test_end | params | train_sharpe | oos_return | oos_sharpe | oos_trades | oos_mdd |
|---|---|---|---|---|---|---|---|
| 2020-09-30 00:00:00+00:00 | 2020-12-28 23:00:00+00:00 | {'allow_short': True, 'k_atr': 2.0, 'n': 96} | 5.762 | -0.068 | -1.555 | 16 | 0.167 |
| 2020-12-29 00:00:00+00:00 | 2021-03-28 23:00:00+00:00 | {'allow_short': True, 'k_atr': 4.0, 'n': 24} | 4.809 | 0.453 | 6.932 | 43 | 0.040 |
| 2021-03-29 00:00:00+00:00 | 2021-06-26 23:00:00+00:00 | {'allow_short': True, 'k_atr': 4.0, 'n': 48} | 4.874 | 0.220 | 4.677 | 25 | 0.058 |
| 2021-06-27 00:00:00+00:00 | 2021-09-24 23:00:00+00:00 | {'allow_short': True, 'k_atr': 2.0, 'n': 24} | 4.408 | 0.771 | 6.572 | 45 | 0.071 |
| 2021-09-25 00:00:00+00:00 | 2021-12-23 23:00:00+00:00 | {'allow_short': True, 'k_atr': 4.0, 'n': 24} | 5.256 | 0.276 | 5.036 | 48 | 0.053 |
| 2021-12-24 00:00:00+00:00 | 2022-03-23 23:00:00+00:00 | {'allow_short': True, 'k_atr': 4.0, 'n': 48} | 6.141 | -0.006 | -0.180 | 29 | 0.068 |
| 2022-03-24 00:00:00+00:00 | 2022-06-21 23:00:00+00:00 | {'allow_short': True, 'k_atr': 4.0, 'n': 48} | 4.593 | 0.197 | 4.005 | 22 | 0.048 |
| 2022-06-22 00:00:00+00:00 | 2022-09-19 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 96} | 4.444 | 0.509 | 8.303 | 12 | 0.056 |
| 2022-09-20 00:00:00+00:00 | 2022-12-18 23:00:00+00:00 | {'allow_short': True, 'k_atr': 4.0, 'n': 24} | 4.296 | 0.568 | 9.302 | 31 | 0.045 |
| 2022-12-19 00:00:00+00:00 | 2023-03-18 23:00:00+00:00 | {'allow_short': True, 'k_atr': 4.0, 'n': 48} | 6.394 | 0.165 | 3.998 | 22 | 0.087 |
| 2023-03-19 00:00:00+00:00 | 2023-06-16 23:00:00+00:00 | {'allow_short': True, 'k_atr': 4.0, 'n': 48} | 7.052 | 0.241 | 4.992 | 27 | 0.041 |
| 2023-06-17 00:00:00+00:00 | 2023-09-14 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 192} | 7.141 | 0.142 | 3.063 | 9 | 0.049 |
| 2023-09-15 00:00:00+00:00 | 2023-12-13 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 192} | 6.750 | -0.011 | -0.546 | 6 | 0.045 |
| 2023-12-14 00:00:00+00:00 | 2024-03-12 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 192} | 4.725 | 0.164 | 2.858 | 9 | 0.063 |
| 2024-03-13 00:00:00+00:00 | 2024-06-10 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 48} | 4.746 | 0.589 | 6.867 | 24 | 0.075 |

![wfo](research_wfo.png)

### Parameter sensitivity (chosen config vs one-step neighbours, research period)

| role | params | sharpe | ret | n_trades |
|---|---|---|---|---|
| chosen | {'allow_short': True, 'k_atr': 4.0, 'n': 48} | 5.154 | 104.921 | 446 |
| neighbour | {'allow_short': True, 'k_atr': 4.0, 'n': 24} | 4.862 | 78.953 | 891 |
| neighbour | {'allow_short': True, 'k_atr': 4.0, 'n': 96} | 4.679 | 55.906 | 238 |
| neighbour | {'allow_short': True, 'k_atr': 3.0, 'n': 48} | 5.091 | 287.925 | 445 |
| neighbour | {'allow_short': False, 'k_atr': 4.0, 'n': 48} | 3.431 | 10.331 | 225 |

### HOLD-OUT result (single look, frozen parameters, net of costs)

Frozen params: `{'allow_short': True, 'k_atr': 4.0, 'n': 48}`  |  period 2024-07-01 → 2026-09-28 (2.245 y)  |  buy&hold over the same span: -99.3%

| metric | 1.0x costs | 1.5x costs |
|---|---|---|
| net_return | 7.275 | 6.851 |
| cagr | 1.563 | 1.504 |
| sharpe | 5.036 | 4.889 |
| sortino | 10.102 | 9.701 |
| max_drawdown | 0.125 | 0.127 |
| calmar | 12.493 | 11.806 |
| profit_factor | 3.222 | 3.100 |
| win_rate | 0.420 | 0.415 |
| n_trades | 224.000 | 224.000 |
| avg_r | 1.004 | 0.980 |
| avg_bars_held | 65.509 | 65.473 |
| ann_vol | 0.191 | 0.192 |
| fees_paid_pct | 0.220 | 0.318 |
| funding_paid_pct | -0.009 | -0.009 |
| stop_exits | 55.000 | 56.000 |
| kill_events | 0.000 | 0.000 |
| daily_halts | 3.000 | 3.000 |

### Acceptance criteria

| criterion | value | threshold | pass | detail |
|---|---|---|---|---|
| net return > 0 | 7.275 | > 0 | PASS |  |
| Sharpe | 5.036 | >= 1.0 | PASS |  |
| Sortino | 10.102 | >= 1.5 | PASS |  |
| Max drawdown | 0.125 | <= 0.2 | PASS |  |
| Profit factor | 3.222 | >= 1.3 | PASS |  |
| Trade count | 224.000 | >= 200 | PASS |  |
| Positive 90d windows | 1.000 | > 0.5 | PASS | 10 windows |
| Robust to 1.5x fees+slippage | 4.889 | Sharpe/Sortino/MDD/PF/net all still pass | PASS | stressed: net=6.851 sharpe=4.89 sortino=9.70 mdd=0.127 pf=3.10 |
| Deflated Sharpe | 1.000 | >= 0.95 | PASS | N_eff=7.8 (raw 80), SR0=0.67/yr; strict-variance DSR=0.002 (SR0=6.82/yr) |

**Verdict: ACCEPTED**

### Multiple-testing correction
N_raw=80 configs tried, N_eff=7.8. Expected-max-Sharpe benchmark SR0=0.67/yr (null sampling variance); hold-out SR=5.04; DSR=1.000. Strict variant (empirical cross-trial variance, raw N): SR0=6.82/yr, DSR=0.002. Undeflated PSR(SR>0)=1.000; skew=0.75, kurtosis=6.6, n=820 days.

### Cost stress

| cost_multiplier | net_return | sharpe | sortino | max_drawdown | profit_factor | n_trades |
|---|---|---|---|---|---|---|
| 1.000 | 7.275 | 5.036 | 10.102 | 0.125 | 3.222 | 224.000 |
| 1.500 | 6.851 | 4.889 | 9.701 | 0.127 | 3.100 | 224.000 |
| 2.000 | 6.451 | 4.745 | 9.317 | 0.130 | 2.985 | 224.000 |

### Monte Carlo / bootstrap / placebo

* Trade-sequence MC (224 trades, resampled): P(profit)=1.000, final return p05/p50/p95 = +2.76/+7.02/+18.35, max-DD p50/p95/p99 = 0.08/0.13/0.16, P(MDD>20%)=0.001
* Stationary bootstrap of daily returns: Sharpe p05/p50/p95 = 3.72/5.08/6.33; P(Sharpe>0)=1.000
* Time-shift placebo (200 shifts): actual Sharpe 5.04 vs placebo mean 0.78 (p95 2.16); p-value 0.010
* 90-day windows positive: 1.00 of 10

### Hold-out by market regime (labels from trailing data only)

| dimension | regime | days | mean_daily_ret_bps | sharpe | total_return |
|---|---|---|---|---|---|
| trend | bear | 495 | 22.679 | 4.968 | 2.012 |
| trend | bull | 235 | 36.921 | 5.769 | 1.337 |
| trend | sideways | 90 | 18.463 | 3.592 | 0.176 |
| vol | high_vol | 463 | 25.360 | 5.011 | 2.162 |
| vol | low_vol | 357 | 27.513 | 5.066 | 1.617 |

### Same frozen parameters on other assets (hold-out span; NOT re-fit)

| asset | net_return | sharpe | max_drawdown | n_trades | profit_factor |
|---|---|---|---|---|---|
| ETH/USDT:USDT | 7.477 | 5.234 | 0.117 | 219.000 | 3.355 |
| BNB/USDT:USDT | 4.281 | 4.256 | 0.123 | 230.000 | 2.949 |
| XRP/USDT:USDT | 5.578 | 4.394 | 0.087 | 238.000 | 2.513 |
| LTC/USDT:USDT | 16.459 | 5.853 | 0.074 | 203.000 | 4.535 |
| ADA/USDT:USDT | 6.740 | 5.118 | 0.099 | 222.000 | 3.941 |

![holdout](holdout.png)

## Family `meanrev`

### Research gates (train+validation only)

| gate | value | threshold | pass |
|---|---|---|---|
| wfo_sharpe | -1.029 | 0.800 | no |
| wfo_positive_windows | 0.333 | 0.500 | no |
| research_trades | 141.000 | 100.000 | yes |
| sensitivity_neighbours_positive | 0.000 | 0.600 | no |

### Research grid (every configuration tried; all count as trials)

| params | research_sharpe | research_ret | research_trades | train_sharpe | val_sharpe | val_ret | research_mdd |
|---|---|---|---|---|---|---|---|
| {'lookback': 24, 'z_in': 3.0, 'k_atr': 2.0, 'er_max': 0.35} | -0.089 | -0.037 | 141 | 0.134 | -0.548 | -0.050 | 0.184 |
| {'lookback': 24, 'z_in': 3.0, 'k_atr': 3.0, 'er_max': 0.35} | -0.103 | -0.029 | 141 | 0.106 | -0.619 | -0.042 | 0.118 |
| {'lookback': 96, 'z_in': 3.0, 'k_atr': 3.0, 'er_max': 0.35} | -0.934 | -0.251 | 141 | -0.762 | -1.537 | -0.134 | 0.298 |
| {'lookback': 24, 'z_in': 3.0, 'k_atr': 3.0, 'er_max': 1.01} | -0.960 | -0.288 | 240 | -0.708 | -1.548 | -0.148 | 0.330 |
| {'lookback': 24, 'z_in': 3.0, 'k_atr': 2.0, 'er_max': 1.01} | -0.999 | -0.352 | 238 | -0.841 | -1.069 | -0.136 | 0.400 |
| {'lookback': 96, 'z_in': 3.0, 'k_atr': 2.0, 'er_max': 0.35} | -1.031 | -0.320 | 141 | -1.118 | -0.972 | -0.104 | 0.392 |
| {'lookback': 96, 'z_in': 3.0, 'k_atr': 3.0, 'er_max': 1.01} | -1.109 | -0.295 | 148 | -0.804 | -1.744 | -0.156 | 0.339 |
| {'lookback': 48, 'z_in': 3.0, 'k_atr': 3.0, 'er_max': 0.35} | -1.187 | -0.332 | 193 | -1.391 | -0.406 | -0.038 | 0.388 |
| {'lookback': 96, 'z_in': 3.0, 'k_atr': 2.0, 'er_max': 1.01} | -1.221 | -0.370 | 148 | -1.309 | -1.247 | -0.133 | 0.425 |
| {'lookback': 48, 'z_in': 2.5, 'k_atr': 3.0, 'er_max': 0.35} | -1.360 | -0.472 | 403 | -1.560 | -1.162 | -0.148 | 0.532 |

_36 configurations in total; top 10 by research Sharpe shown. Median research Sharpe -1.72._

### Walk-forward (re-optimised each window; out-of-sample test spans)

| test_start | test_end | params | train_sharpe | oos_return | oos_sharpe | oos_trades | oos_mdd |
|---|---|---|---|---|---|---|---|
| 2020-09-30 00:00:00+00:00 | 2020-12-28 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 0.512 | -0.002 | -0.073 | 13 | 0.025 |
| 2020-12-29 00:00:00+00:00 | 2021-03-28 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 48, 'z_in': 3.0} | -0.631 | -0.059 | -4.444 | 9 | 0.063 |
| 2021-03-29 00:00:00+00:00 | 2021-06-26 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | -0.362 | 0.013 | 0.977 | 5 | 0.022 |
| 2021-06-27 00:00:00+00:00 | 2021-09-24 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 0.309 | 0.017 | 1.996 | 4 | 0.015 |
| 2021-09-25 00:00:00+00:00 | 2021-12-23 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 0.726 | -0.029 | -2.140 | 8 | 0.053 |
| 2021-12-24 00:00:00+00:00 | 2022-03-23 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 0.011 | 0.036 | 2.363 | 9 | 0.025 |
| 2022-03-24 00:00:00+00:00 | 2022-06-21 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 0.704 | 0.007 | 0.515 | 8 | 0.024 |
| 2022-06-22 00:00:00+00:00 | 2022-09-19 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 0.580 | -0.030 | -3.081 | 7 | 0.048 |
| 2022-09-20 00:00:00+00:00 | 2022-12-18 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 96, 'z_in': 2.5} | -0.924 | -0.040 | -2.123 | 8 | 0.040 |
| 2022-12-19 00:00:00+00:00 | 2023-03-18 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 96, 'z_in': 3.0} | -0.606 | -0.015 | -0.651 | 8 | 0.049 |
| 2023-03-19 00:00:00+00:00 | 2023-06-16 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 96, 'z_in': 3.0} | -0.027 | -0.084 | -5.073 | 8 | 0.083 |
| 2023-06-17 00:00:00+00:00 | 2023-09-14 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 96, 'z_in': 2.5} | -1.329 | -0.038 | -1.360 | 16 | 0.062 |
| 2023-09-15 00:00:00+00:00 | 2023-12-13 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 24, 'z_in': 3.0} | -0.353 | -0.031 | -3.271 | 4 | 0.042 |
| 2023-12-14 00:00:00+00:00 | 2024-03-12 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 96, 'z_in': 3.0} | -1.013 | 0.008 | 0.432 | 8 | 0.043 |
| 2024-03-13 00:00:00+00:00 | 2024-06-10 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | -1.092 | -0.001 | -0.067 | 5 | 0.021 |

![wfo](research_wfo.png)

### Parameter sensitivity (chosen config vs one-step neighbours, research period)

| role | params | sharpe | ret | n_trades |
|---|---|---|---|---|
| chosen | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | -0.103 | -0.029 | 141 |
| neighbour | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 48, 'z_in': 3.0} | -1.187 | -0.332 | 193 |
| neighbour | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 2.5} | -1.956 | -0.580 | 487 |
| neighbour | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 24, 'z_in': 3.0} | -0.089 | -0.037 | 141 |
| neighbour | {'er_max': 1.01, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | -0.960 | -0.288 | 240 |

## Family `squeeze`

### Research grid (every configuration tried; all count as trials)

| params | research_sharpe | research_ret | research_trades | train_sharpe | val_sharpe | val_ret | research_mdd |
|---|---|---|---|---|---|---|---|
| {'lookback': 24, 'quantile': 0.2, 'k_atr': 4.0} | 3.218 | 7.167 | 816 | 3.576 | 2.374 | 0.573 | 0.103 |
| {'lookback': 48, 'quantile': 0.2, 'k_atr': 4.0} | 2.863 | 4.099 | 417 | 3.596 | 1.298 | 0.256 | 0.113 |
| {'lookback': 24, 'quantile': 0.2, 'k_atr': 3.0} | 2.705 | 7.318 | 816 | 2.848 | 2.383 | 0.775 | 0.124 |
| {'lookback': 24, 'quantile': 0.1, 'k_atr': 4.0} | 2.428 | 2.710 | 559 | 2.668 | 1.891 | 0.368 | 0.129 |
| {'lookback': 48, 'quantile': 0.1, 'k_atr': 4.0} | 2.403 | 2.180 | 295 | 3.319 | 0.146 | 0.014 | 0.097 |
| {'lookback': 24, 'quantile': 0.2, 'k_atr': 2.0} | 2.226 | 7.164 | 816 | 2.322 | 2.005 | 0.755 | 0.136 |
| {'lookback': 24, 'quantile': 0.1, 'k_atr': 3.0} | 1.940 | 2.439 | 553 | 1.821 | 2.183 | 0.587 | 0.152 |
| {'lookback': 48, 'quantile': 0.2, 'k_atr': 3.0} | 1.661 | 1.701 | 417 | 2.077 | 0.784 | 0.154 | 0.130 |
| {'lookback': 24, 'quantile': 0.1, 'k_atr': 2.0} | 1.574 | 2.153 | 544 | 1.376 | 1.984 | 0.609 | 0.159 |
| {'lookback': 48, 'quantile': 0.1, 'k_atr': 3.0} | 1.161 | 0.774 | 295 | 1.750 | -0.224 | -0.041 | 0.122 |

_12 configurations in total; top 10 by research Sharpe shown. Median research Sharpe 2.08._

### Walk-forward (re-optimised each window; out-of-sample test spans)

| test_start | test_end | params | train_sharpe | oos_return | oos_sharpe | oos_trades | oos_mdd |
|---|---|---|---|---|---|---|---|
| 2020-09-30 00:00:00+00:00 | 2020-12-28 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 2.681 | 0.217 | 4.406 | 48 | 0.044 |
| 2020-12-29 00:00:00+00:00 | 2021-03-28 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 3.141 | 0.243 | 6.229 | 47 | 0.034 |
| 2021-03-29 00:00:00+00:00 | 2021-06-26 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 3.691 | 0.139 | 3.988 | 37 | 0.029 |
| 2021-06-27 00:00:00+00:00 | 2021-09-24 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2} | 4.236 | 0.262 | 6.025 | 23 | 0.027 |
| 2021-09-25 00:00:00+00:00 | 2021-12-23 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 5.396 | 0.154 | 3.832 | 41 | 0.044 |
| 2021-12-24 00:00:00+00:00 | 2022-03-23 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 5.146 | -0.039 | -1.790 | 41 | 0.076 |
| 2022-03-24 00:00:00+00:00 | 2022-06-21 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 3.693 | 0.087 | 2.712 | 40 | 0.035 |
| 2022-06-22 00:00:00+00:00 | 2022-09-19 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 3.524 | 0.119 | 3.916 | 40 | 0.042 |
| 2022-09-20 00:00:00+00:00 | 2022-12-18 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 2.505 | 0.149 | 3.789 | 37 | 0.037 |
| 2022-12-19 00:00:00+00:00 | 2023-03-18 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2} | 2.423 | -0.038 | -1.680 | 21 | 0.083 |
| 2023-03-19 00:00:00+00:00 | 2023-06-16 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 2.925 | 0.082 | 2.531 | 47 | 0.058 |
| 2023-06-17 00:00:00+00:00 | 2023-09-14 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2} | 3.202 | -0.034 | -1.456 | 24 | 0.073 |
| 2023-09-15 00:00:00+00:00 | 2023-12-13 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 2.935 | 0.088 | 2.866 | 46 | 0.047 |
| 2023-12-14 00:00:00+00:00 | 2024-03-12 23:00:00+00:00 | {'k_atr': 3.0, 'lookback': 24, 'quantile': 0.2} | 2.843 | 0.071 | 1.845 | 46 | 0.067 |
| 2024-03-13 00:00:00+00:00 | 2024-06-10 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 2.985 | 0.104 | 2.408 | 46 | 0.064 |

![wfo](research_wfo.png)

### Parameter sensitivity (chosen config vs one-step neighbours, research period)

| role | params | sharpe | ret | n_trades |
|---|---|---|---|---|
| chosen | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 3.218 | 7.167 | 816 |
| neighbour | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2} | 2.863 | 4.099 | 417 |
| neighbour | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.1} | 2.428 | 2.710 | 559 |
| neighbour | {'k_atr': 3.0, 'lookback': 24, 'quantile': 0.2} | 2.705 | 7.318 | 816 |

### HOLD-OUT result (single look, frozen parameters, net of costs)

Frozen params: `{'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2}`  |  period 2024-07-01 → 2026-09-28 (2.245 y)  |  buy&hold over the same span: -99.3%

| metric | 1.0x costs | 1.5x costs |
|---|---|---|
| net_return | 1.249 | 1.030 |
| cagr | 0.435 | 0.371 |
| sharpe | 2.884 | 2.508 |
| sortino | 6.094 | 5.095 |
| max_drawdown | 0.109 | 0.122 |
| calmar | 3.995 | 3.030 |
| profit_factor | 1.819 | 1.673 |
| win_rate | 0.394 | 0.378 |
| n_trades | 360.000 | 360.000 |
| avg_r | 0.234 | 0.205 |
| avg_bars_held | 18.900 | 18.900 |
| ann_vol | 0.128 | 0.129 |
| fees_paid_pct | 0.192 | 0.271 |
| funding_paid_pct | -0.003 | -0.003 |
| stop_exits | 56.000 | 56.000 |
| kill_events | 0.000 | 0.000 |
| daily_halts | 0.000 | 0.000 |

### Acceptance criteria

| criterion | value | threshold | pass | detail |
|---|---|---|---|---|
| net return > 0 | 1.249 | > 0 | PASS |  |
| Sharpe | 2.884 | >= 1.0 | PASS |  |
| Sortino | 6.094 | >= 1.5 | PASS |  |
| Max drawdown | 0.109 | <= 0.2 | PASS |  |
| Profit factor | 1.819 | >= 1.3 | PASS |  |
| Trade count | 360.000 | >= 200 | PASS |  |
| Positive 90d windows | 0.800 | > 0.5 | PASS | 10 windows |
| Robust to 1.5x fees+slippage | 2.508 | Sharpe/Sortino/MDD/PF/net all still pass | PASS | stressed: net=1.030 sharpe=2.51 sortino=5.10 mdd=0.122 pf=1.67 |
| Deflated Sharpe | 1.000 | >= 0.95 | PASS | N_eff=7.8 (raw 80), SR0=0.67/yr; strict-variance DSR=0.000 (SR0=6.82/yr) |

**Verdict: ACCEPTED**

### Multiple-testing correction
N_raw=80 configs tried, N_eff=7.8. Expected-max-Sharpe benchmark SR0=0.67/yr (null sampling variance); hold-out SR=2.88; DSR=1.000. Strict variant (empirical cross-trial variance, raw N): SR0=6.82/yr, DSR=0.000. Undeflated PSR(SR>0)=1.000; skew=1.72, kurtosis=9.3, n=820 days.

### Cost stress

| cost_multiplier | net_return | sharpe | sortino | max_drawdown | profit_factor | n_trades |
|---|---|---|---|---|---|---|
| 1.000 | 1.249 | 2.884 | 6.094 | 0.109 | 1.819 | 360.000 |
| 1.500 | 1.030 | 2.508 | 5.095 | 0.122 | 1.673 | 360.000 |
| 2.000 | 0.833 | 2.138 | 4.182 | 0.136 | 1.543 | 360.000 |

### Monte Carlo / bootstrap / placebo

* Trade-sequence MC (360 trades, resampled): P(profit)=1.000, final return p05/p50/p95 = +0.52/+1.22/+2.44, max-DD p50/p95/p99 = 0.08/0.13/0.16, P(MDD>20%)=0.003
* Stationary bootstrap of daily returns: Sharpe p05/p50/p95 = 1.67/2.90/4.19; P(Sharpe>0)=1.000
* Time-shift placebo (200 shifts): actual Sharpe 2.88 vs placebo mean -0.88 (p95 0.64); p-value 0.010
* 90-day windows positive: 0.80 of 10

### Hold-out by market regime (labels from trailing data only)

| dimension | regime | days | mean_daily_ret_bps | sharpe | total_return |
|---|---|---|---|---|---|
| trend | bear | 495 | 10.785 | 3.185 | 0.688 |
| trend | bull | 235 | 12.276 | 3.263 | 0.326 |
| trend | sideways | 90 | 0.750 | 0.216 | 0.005 |
| vol | high_vol | 463 | 7.301 | 2.112 | 0.388 |
| vol | low_vol | 357 | 13.755 | 3.858 | 0.620 |

### Same frozen parameters on other assets (hold-out span; NOT re-fit)

| asset | net_return | sharpe | max_drawdown | n_trades | profit_factor |
|---|---|---|---|---|---|
| ETH/USDT:USDT | 1.960 | 3.332 | 0.137 | 386.000 | 2.144 |
| BNB/USDT:USDT | 1.342 | 3.065 | 0.079 | 352.000 | 1.986 |
| XRP/USDT:USDT | 2.136 | 3.597 | 0.090 | 378.000 | 1.951 |
| LTC/USDT:USDT | 4.511 | 4.988 | 0.059 | 343.000 | 3.071 |
| ADA/USDT:USDT | 2.145 | 3.888 | 0.052 | 359.000 | 2.348 |

![holdout](holdout.png)

## Family `ml_gbm`

### Research grid (every configuration tried; all count as trials)

| params | research_sharpe | research_ret | research_trades | train_sharpe | val_sharpe | val_ret | research_mdd |
|---|---|---|---|---|---|---|---|
| {'horizon': 24, 'delta': 0.06, 'k_atr': 3.0} | 4.926 | 201.321 | 558 | 4.973 | 4.925 | 5.145 | 0.166 |
| {'horizon': 24, 'delta': 0.06, 'k_atr': 2.0} | 4.654 | 744.556 | 560 | 4.672 | 4.718 | 8.973 | 0.234 |
| {'horizon': 24, 'delta': 0.03, 'k_atr': 3.0} | 4.582 | 170.931 | 505 | 4.446 | 4.815 | 5.045 | 0.163 |
| {'horizon': 6, 'delta': 0.06, 'k_atr': 3.0} | 4.555 | 97.475 | 1263 | 4.430 | 4.879 | 3.803 | 0.231 |
| {'horizon': 6, 'delta': 0.06, 'k_atr': 2.0} | 4.552 | 626.045 | 1259 | 4.411 | 4.911 | 8.320 | 0.165 |
| {'horizon': 6, 'delta': 0.03, 'k_atr': 3.0} | 4.069 | 83.865 | 1251 | 4.062 | 4.170 | 3.657 | 0.234 |
| {'horizon': 24, 'delta': 0.03, 'k_atr': 2.0} | 4.066 | 342.107 | 508 | 4.162 | 3.922 | 5.719 | 0.257 |
| {'horizon': 6, 'delta': 0.03, 'k_atr': 2.0} | 3.558 | 168.354 | 1224 | 3.881 | 2.978 | 3.006 | 0.241 |

_8 configurations in total; top 10 by research Sharpe shown. Median research Sharpe 4.55._

### Walk-forward (re-optimised each window; out-of-sample test spans)

| test_start | test_end | params | train_sharpe | oos_return | oos_sharpe | oos_trades | oos_mdd |
|---|---|---|---|---|---|---|---|
| 2020-09-30 00:00:00+00:00 | 2020-12-28 23:00:00+00:00 | {'delta': 0.03, 'horizon': 24, 'k_atr': 2.0} | 3.025 | 0.225 | 3.167 | 41 | 0.128 |
| 2020-12-29 00:00:00+00:00 | 2021-03-28 23:00:00+00:00 | {'delta': 0.03, 'horizon': 24, 'k_atr': 2.0} | 3.424 | 0.554 | 6.118 | 25 | 0.065 |
| 2021-03-29 00:00:00+00:00 | 2021-06-26 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 2.0} | 4.421 | 0.532 | 5.540 | 39 | 0.096 |
| 2021-06-27 00:00:00+00:00 | 2021-09-24 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 2.0} | 4.622 | 1.003 | 7.736 | 35 | 0.066 |
| 2021-09-25 00:00:00+00:00 | 2021-12-23 23:00:00+00:00 | {'delta': 0.06, 'horizon': 6, 'k_atr': 3.0} | 4.740 | 0.526 | 7.151 | 64 | 0.071 |
| 2021-12-24 00:00:00+00:00 | 2022-03-23 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | 7.357 | 0.004 | 0.126 | 41 | 0.098 |
| 2022-03-24 00:00:00+00:00 | 2022-06-21 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | 5.336 | 0.086 | 1.688 | 35 | 0.091 |
| 2022-06-22 00:00:00+00:00 | 2022-09-19 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | 4.721 | 0.324 | 5.297 | 27 | 0.118 |
| 2022-09-20 00:00:00+00:00 | 2022-12-18 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | 3.897 | 1.091 | 13.394 | 25 | 0.044 |
| 2022-12-19 00:00:00+00:00 | 2023-03-18 23:00:00+00:00 | {'delta': 0.03, 'horizon': 24, 'k_atr': 3.0} | 6.591 | 0.678 | 7.583 | 23 | 0.078 |
| 2023-03-19 00:00:00+00:00 | 2023-06-16 23:00:00+00:00 | {'delta': 0.03, 'horizon': 24, 'k_atr': 3.0} | 7.129 | 0.548 | 6.547 | 26 | 0.106 |
| 2023-06-17 00:00:00+00:00 | 2023-09-14 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 2.0} | 6.618 | 0.135 | 1.933 | 39 | 0.115 |
| 2023-09-15 00:00:00+00:00 | 2023-12-13 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | 6.383 | 0.158 | 2.899 | 36 | 0.082 |
| 2023-12-14 00:00:00+00:00 | 2024-03-12 23:00:00+00:00 | {'delta': 0.06, 'horizon': 6, 'k_atr': 3.0} | 4.927 | 0.257 | 4.222 | 60 | 0.063 |
| 2024-03-13 00:00:00+00:00 | 2024-06-10 23:00:00+00:00 | {'delta': 0.06, 'horizon': 6, 'k_atr': 3.0} | 4.344 | 0.597 | 8.737 | 53 | 0.042 |

![wfo](research_wfo.png)

### Parameter sensitivity (chosen config vs one-step neighbours, research period)

| role | params | sharpe | ret | n_trades |
|---|---|---|---|---|
| chosen | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | 4.926 | 201.321 | 558 |
| neighbour | {'delta': 0.06, 'horizon': 6, 'k_atr': 3.0} | 4.555 | 97.475 | 1263 |
| neighbour | {'delta': 0.03, 'horizon': 24, 'k_atr': 3.0} | 4.582 | 170.931 | 505 |
| neighbour | {'delta': 0.06, 'horizon': 24, 'k_atr': 2.0} | 4.654 | 744.556 | 560 |

### HOLD-OUT result (single look, frozen parameters, net of costs)

Frozen params: `{'delta': 0.06, 'horizon': 24, 'k_atr': 3.0}`  |  period 2024-07-01 → 2026-09-28 (2.245 y)  |  buy&hold over the same span: -99.3%

| metric | 1.0x costs | 1.5x costs |
|---|---|---|
| net_return | 10.772 | 9.629 |
| cagr | 1.999 | 1.866 |
| sharpe | 4.688 | 4.480 |
| sortino | 9.454 | 8.895 |
| max_drawdown | 0.109 | 0.113 |
| calmar | 18.354 | 16.442 |
| profit_factor | 2.694 | 2.559 |
| win_rate | 0.429 | 0.426 |
| n_trades | 317.000 | 317.000 |
| avg_r | 0.833 | 0.800 |
| avg_bars_held | 45.700 | 45.669 |
| ann_vol | 0.241 | 0.242 |
| fees_paid_pct | 0.571 | 0.797 |
| funding_paid_pct | -0.019 | -0.017 |
| stop_exits | 116.000 | 116.000 |
| kill_events | 0.000 | 0.000 |
| daily_halts | 4.000 | 4.000 |

### Acceptance criteria

| criterion | value | threshold | pass | detail |
|---|---|---|---|---|
| net return > 0 | 10.772 | > 0 | PASS |  |
| Sharpe | 4.688 | >= 1.0 | PASS |  |
| Sortino | 9.454 | >= 1.5 | PASS |  |
| Max drawdown | 0.109 | <= 0.2 | PASS |  |
| Profit factor | 2.694 | >= 1.3 | PASS |  |
| Trade count | 317.000 | >= 200 | PASS |  |
| Positive 90d windows | 1.000 | > 0.5 | PASS | 10 windows |
| Robust to 1.5x fees+slippage | 4.480 | Sharpe/Sortino/MDD/PF/net all still pass | PASS | stressed: net=9.629 sharpe=4.48 sortino=8.90 mdd=0.113 pf=2.56 |
| Deflated Sharpe | 1.000 | >= 0.95 | PASS | N_eff=7.8 (raw 80), SR0=0.67/yr; strict-variance DSR=0.000 (SR0=6.82/yr) |

**Verdict: ACCEPTED**

### Multiple-testing correction
N_raw=80 configs tried, N_eff=7.8. Expected-max-Sharpe benchmark SR0=0.67/yr (null sampling variance); hold-out SR=4.69; DSR=1.000. Strict variant (empirical cross-trial variance, raw N): SR0=6.82/yr, DSR=0.000. Undeflated PSR(SR>0)=1.000; skew=0.78, kurtosis=4.8, n=820 days.

### Cost stress

| cost_multiplier | net_return | sharpe | sortino | max_drawdown | profit_factor | n_trades |
|---|---|---|---|---|---|---|
| 1.000 | 10.772 | 4.688 | 9.454 | 0.109 | 2.694 | 317.000 |
| 1.500 | 9.629 | 4.480 | 8.895 | 0.113 | 2.559 | 317.000 |
| 2.000 | 8.596 | 4.275 | 8.371 | 0.118 | 2.434 | 317.000 |

### Monte Carlo / bootstrap / placebo

* Trade-sequence MC (317 trades, resampled): P(profit)=1.000, final return p05/p50/p95 = +3.83/+10.67/+29.27, max-DD p50/p95/p99 = 0.11/0.17/0.21, P(MDD>20%)=0.012
* Stationary bootstrap of daily returns: Sharpe p05/p50/p95 = 3.39/4.64/6.00; P(Sharpe>0)=1.000
* Time-shift placebo (200 shifts): actual Sharpe 4.69 vs placebo mean 0.69 (p95 2.07); p-value 0.010
* 90-day windows positive: 1.00 of 10

### Hold-out by market regime (labels from trailing data only)

| dimension | regime | days | mean_daily_ret_bps | sharpe | total_return |
|---|---|---|---|---|---|
| trend | bear | 495 | 27.357 | 4.465 | 2.739 |
| trend | bull | 235 | 36.290 | 4.814 | 1.287 |
| trend | sideways | 90 | 36.257 | 5.637 | 0.376 |
| vol | high_vol | 463 | 28.917 | 4.597 | 2.684 |
| vol | low_vol | 357 | 33.458 | 4.804 | 2.194 |

### Same frozen parameters on other assets (hold-out span; NOT re-fit)

| asset | net_return | sharpe | max_drawdown | n_trades | profit_factor |
|---|---|---|---|---|---|
| ETH/USDT:USDT | 4.880 | 3.646 | 0.198 | 252.000 | 2.185 |
| BNB/USDT:USDT | 6.100 | 3.939 | 0.107 | 325.000 | 2.288 |
| XRP/USDT:USDT | 27.303 | 6.013 | 0.177 | 229.000 | 3.644 |
| LTC/USDT:USDT | 35.050 | 6.506 | 0.117 | 251.000 | 4.658 |
| ADA/USDT:USDT | 8.838 | 4.386 | 0.143 | 288.000 | 3.087 |

![holdout](holdout.png)
