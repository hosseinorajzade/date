# SYNTHETIC planted weak trend (seed 0) — pipeline validation

> Synthetic data. Demonstrates the pipeline's behaviour; says nothing about real markets.

Trials registered: **80** configurations (effective independent ≈ 8.5); by family: {'donchian': 24, 'meanrev': 36, 'squeeze': 12, 'ml_gbm': 8}

## Summary

| family | stage | params | net | sharpe | sortino | mdd | PF | trades | DSR | accepted |
|---|---|---|---|---|---|---|---|---|---|---|
| donchian | hold-out | {'allow_short': True, 'k_atr': 4.0, 'n': 96} | 0.726 | 1.584 | 2.677 | 0.143 | 1.685 | 144.000 | 0.921 | no |
| meanrev | rejected at research | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | n/a | n/a | n/a | n/a | n/a | n/a | n/a | no |
| squeeze | hold-out | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.1} | 0.314 | 1.366 | 2.680 | 0.069 | 1.410 | 251.000 | 0.869 | no |
| ml_gbm | hold-out | {'delta': 0.03, 'horizon': 24, 'k_atr': 3.0} | 0.386 | 0.790 | 1.271 | 0.160 | 1.146 | 400.000 | 0.573 | no |

## Family `donchian`

### Research grid (every configuration tried; all count as trials)

| params | research_sharpe | research_ret | research_trades | train_sharpe | val_sharpe | val_ret | research_mdd |
|---|---|---|---|---|---|---|---|
| {'n': 96, 'k_atr': 3.0, 'allow_short': True} | 2.813 | 13.249 | 276 | 3.198 | 1.865 | 0.609 | 0.120 |
| {'n': 96, 'k_atr': 4.0, 'allow_short': True} | 2.671 | 7.208 | 278 | 2.996 | 1.920 | 0.551 | 0.106 |
| {'n': 96, 'k_atr': 2.0, 'allow_short': True} | 2.451 | 15.185 | 280 | 2.802 | 1.595 | 0.633 | 0.166 |
| {'n': 192, 'k_atr': 4.0, 'allow_short': True} | 2.249 | 3.506 | 144 | 2.478 | 1.768 | 0.427 | 0.115 |
| {'n': 48, 'k_atr': 4.0, 'allow_short': True} | 2.158 | 4.442 | 522 | 2.559 | 1.268 | 0.350 | 0.138 |
| {'n': 192, 'k_atr': 2.0, 'allow_short': True} | 1.956 | 6.234 | 160 | 2.330 | 1.399 | 0.467 | 0.214 |
| {'n': 48, 'k_atr': 3.0, 'allow_short': True} | 1.942 | 5.284 | 521 | 2.319 | 1.060 | 0.331 | 0.176 |
| {'n': 192, 'k_atr': 3.0, 'allow_short': True} | 1.876 | 3.398 | 145 | 2.267 | 0.976 | 0.238 | 0.187 |
| {'n': 24, 'k_atr': 4.0, 'allow_short': True} | 1.623 | 2.555 | 1006 | 1.851 | 1.072 | 0.267 | 0.169 |
| {'n': 96, 'k_atr': 3.0, 'allow_short': False} | 1.604 | 1.906 | 134 | 1.900 | 0.836 | 0.157 | 0.143 |

_24 configurations in total; top 10 by research Sharpe shown. Median research Sharpe 1.48._

### Walk-forward (re-optimised each window; out-of-sample test spans)

| test_start | test_end | params | train_sharpe | oos_return | oos_sharpe | oos_trades | oos_mdd |
|---|---|---|---|---|---|---|---|
| 2020-09-30 00:00:00+00:00 | 2020-12-28 23:00:00+00:00 | {'allow_short': True, 'k_atr': 2.0, 'n': 192} | 2.804 | 0.147 | 2.369 | 8 | 0.049 |
| 2020-12-29 00:00:00+00:00 | 2021-03-28 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 192} | 3.238 | 0.210 | 3.278 | 9 | 0.067 |
| 2021-03-29 00:00:00+00:00 | 2021-06-26 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 192} | 3.133 | -0.020 | -0.368 | 10 | 0.086 |
| 2021-06-27 00:00:00+00:00 | 2021-09-24 23:00:00+00:00 | {'allow_short': False, 'k_atr': 2.0, 'n': 24} | 2.681 | 0.213 | 3.818 | 22 | 0.074 |
| 2021-09-25 00:00:00+00:00 | 2021-12-23 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 192} | 3.586 | 0.058 | 1.027 | 7 | 0.144 |
| 2021-12-24 00:00:00+00:00 | 2022-03-23 23:00:00+00:00 | {'allow_short': True, 'k_atr': 4.0, 'n': 96} | 3.331 | 0.053 | 1.652 | 13 | 0.049 |
| 2022-03-24 00:00:00+00:00 | 2022-06-21 23:00:00+00:00 | {'allow_short': True, 'k_atr': 2.0, 'n': 192} | 2.596 | -0.113 | -4.744 | 12 | 0.119 |
| 2022-06-22 00:00:00+00:00 | 2022-09-19 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 96} | 3.159 | 0.412 | 6.838 | 11 | 0.041 |
| 2022-09-20 00:00:00+00:00 | 2022-12-18 23:00:00+00:00 | {'allow_short': True, 'k_atr': 4.0, 'n': 96} | 3.266 | 0.327 | 8.940 | 6 | 0.029 |
| 2022-12-19 00:00:00+00:00 | 2023-03-18 23:00:00+00:00 | {'allow_short': True, 'k_atr': 4.0, 'n': 96} | 4.717 | 0.019 | 0.637 | 17 | 0.080 |
| 2023-03-19 00:00:00+00:00 | 2023-06-16 23:00:00+00:00 | {'allow_short': True, 'k_atr': 4.0, 'n': 96} | 4.238 | 0.061 | 1.578 | 15 | 0.065 |
| 2023-06-17 00:00:00+00:00 | 2023-09-14 23:00:00+00:00 | {'allow_short': True, 'k_atr': 4.0, 'n': 96} | 4.279 | 0.015 | 0.510 | 20 | 0.064 |
| 2023-09-15 00:00:00+00:00 | 2023-12-13 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 192} | 2.184 | 0.043 | 1.120 | 9 | 0.108 |
| 2023-12-14 00:00:00+00:00 | 2024-03-12 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 192} | 1.489 | 0.041 | 1.256 | 8 | 0.065 |
| 2024-03-13 00:00:00+00:00 | 2024-06-10 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 24} | 2.064 | 0.011 | 0.226 | 62 | 0.118 |

![wfo](research_wfo.png)

### Parameter sensitivity (chosen config vs one-step neighbours, research period)

| role | params | sharpe | ret | n_trades |
|---|---|---|---|---|
| chosen | {'allow_short': True, 'k_atr': 4.0, 'n': 96} | 2.671 | 7.208 | 278 |
| neighbour | {'allow_short': True, 'k_atr': 4.0, 'n': 48} | 2.158 | 4.442 | 522 |
| neighbour | {'allow_short': True, 'k_atr': 4.0, 'n': 192} | 2.249 | 3.506 | 144 |
| neighbour | {'allow_short': True, 'k_atr': 3.0, 'n': 96} | 2.813 | 13.249 | 276 |
| neighbour | {'allow_short': False, 'k_atr': 4.0, 'n': 96} | 1.502 | 1.368 | 135 |

### HOLD-OUT result (single look, frozen parameters, net of costs)

Frozen params: `{'allow_short': True, 'k_atr': 4.0, 'n': 96}`  |  period 2024-07-01 → 2026-09-28 (2.245 y)  |  buy&hold over the same span: -97.7%

| metric | 1.0x costs | 1.5x costs |
|---|---|---|
| net_return | 0.726 | 0.670 |
| cagr | 0.275 | 0.257 |
| sharpe | 1.584 | 1.489 |
| sortino | 2.677 | 2.499 |
| max_drawdown | 0.143 | 0.146 |
| calmar | 1.931 | 1.763 |
| profit_factor | 1.685 | 1.626 |
| win_rate | 0.368 | 0.368 |
| n_trades | 144.000 | 144.000 |
| avg_r | 0.413 | 0.389 |
| avg_bars_held | 82.111 | 82.104 |
| ann_vol | 0.162 | 0.162 |
| fees_paid_pct | 0.054 | 0.080 |
| funding_paid_pct | 0.001 | 0.001 |
| stop_exits | 61.000 | 61.000 |
| kill_events | 0.000 | 0.000 |
| daily_halts | 2.000 | 2.000 |

### Acceptance criteria

| criterion | value | threshold | pass | detail |
|---|---|---|---|---|
| net return > 0 | 0.726 | > 0 | PASS |  |
| Sharpe | 1.584 | >= 1.0 | PASS |  |
| Sortino | 2.677 | >= 1.5 | PASS |  |
| Max drawdown | 0.143 | <= 0.2 | PASS |  |
| Profit factor | 1.685 | >= 1.3 | PASS |  |
| Trade count | 144.000 | >= 200 | FAIL |  |
| Positive 90d windows | 0.700 | > 0.5 | PASS | 10 windows |
| Robust to 1.5x fees+slippage | 1.489 | Sharpe/Sortino/MDD/PF/net all still pass | PASS | stressed: net=0.670 sharpe=1.49 sortino=2.50 mdd=0.146 pf=1.63 |
| Deflated Sharpe | 0.921 | >= 0.95 | FAIL | N_eff=8.5 (raw 80), SR0=0.67/yr; strict-variance DSR=0.006 (SR0=3.22/yr) |

**Verdict: NOT ACCEPTED**

### Multiple-testing correction
N_raw=80 configs tried, N_eff=8.5. Expected-max-Sharpe benchmark SR0=0.67/yr (null sampling variance); hold-out SR=1.58; DSR=0.921. Strict variant (empirical cross-trial variance, raw N): SR0=3.22/yr, DSR=0.006. Undeflated PSR(SR>0)=0.993; skew=0.89, kurtosis=9.6, n=820 days.

### Cost stress

| cost_multiplier | net_return | sharpe | sortino | max_drawdown | profit_factor | n_trades |
|---|---|---|---|---|---|---|
| 1.000 | 0.726 | 1.584 | 2.677 | 0.143 | 1.685 | 144.000 |
| 1.500 | 0.670 | 1.489 | 2.499 | 0.146 | 1.626 | 144.000 |
| 2.000 | 0.615 | 1.394 | 2.325 | 0.149 | 1.571 | 144.000 |

### Monte Carlo / bootstrap / placebo

* Trade-sequence MC (144 trades, resampled): P(profit)=0.970, final return p05/p50/p95 = +0.07/+0.70/+1.86, max-DD p50/p95/p99 = 0.12/0.22/0.28, P(MDD>20%)=0.088
* Stationary bootstrap of daily returns: Sharpe p05/p50/p95 = 0.42/1.62/2.70; P(Sharpe>0)=0.989
* Time-shift placebo (200 shifts): actual Sharpe 1.58 vs placebo mean 0.06 (p95 1.13); p-value 0.025
* 90-day windows positive: 0.70 of 10

### Hold-out by market regime (labels from trailing data only)

| dimension | regime | days | mean_daily_ret_bps | sharpe | total_return |
|---|---|---|---|---|---|
| trend | bear | 489 | 6.285 | 1.492 | 0.338 |
| trend | bull | 122 | 12.899 | 2.328 | 0.162 |
| trend | sideways | 209 | 5.271 | 1.260 | 0.109 |
| vol | high_vol | 484 | 6.868 | 1.757 | 0.376 |
| vol | low_vol | 336 | 7.217 | 1.420 | 0.255 |

### Same frozen parameters on other assets (hold-out span; NOT re-fit)

| asset | net_return | sharpe | max_drawdown | n_trades | profit_factor |
|---|---|---|---|---|---|
| ETH/USDT:USDT | 0.755 | 1.685 | 0.158 | 136.000 | 1.697 |
| BNB/USDT:USDT | 0.173 | 0.612 | 0.250 | 142.000 | 1.204 |
| XRP/USDT:USDT | 1.545 | 2.728 | 0.157 | 130.000 | 2.215 |
| LTC/USDT:USDT | 1.545 | 2.598 | 0.109 | 134.000 | 2.207 |
| ADA/USDT:USDT | 0.168 | 0.585 | 0.176 | 144.000 | 1.202 |

![holdout](holdout.png)

## Family `meanrev`

### Research gates (train+validation only)

| gate | value | threshold | pass |
|---|---|---|---|
| wfo_sharpe | -0.763 | 0.800 | no |
| wfo_positive_windows | 0.400 | 0.500 | no |
| research_trades | 163.000 | 100.000 | yes |
| sensitivity_neighbours_positive | 0.000 | 0.600 | no |

### Research grid (every configuration tried; all count as trials)

| params | research_sharpe | research_ret | research_trades | train_sharpe | val_sharpe | val_ret | research_mdd |
|---|---|---|---|---|---|---|---|
| {'lookback': 24, 'z_in': 3.0, 'k_atr': 3.0, 'er_max': 0.35} | 0.025 | -0.000 | 163 | 0.307 | -0.611 | -0.049 | 0.103 |
| {'lookback': 24, 'z_in': 3.0, 'k_atr': 2.0, 'er_max': 0.35} | -0.164 | -0.068 | 161 | 0.026 | -0.665 | -0.069 | 0.164 |
| {'lookback': 24, 'z_in': 3.0, 'k_atr': 3.0, 'er_max': 1.01} | -0.367 | -0.125 | 258 | -0.160 | -0.866 | -0.088 | 0.172 |
| {'lookback': 24, 'z_in': 3.0, 'k_atr': 2.0, 'er_max': 1.01} | -0.596 | -0.240 | 256 | -0.587 | -0.710 | -0.096 | 0.296 |
| {'lookback': 96, 'z_in': 3.0, 'k_atr': 3.0, 'er_max': 0.35} | -0.725 | -0.231 | 161 | -0.672 | -0.954 | -0.095 | 0.313 |
| {'lookback': 48, 'z_in': 2.0, 'k_atr': 3.0, 'er_max': 1.01} | -0.742 | -0.359 | 716 | -0.794 | -0.730 | -0.124 | 0.450 |
| {'lookback': 48, 'z_in': 3.0, 'k_atr': 3.0, 'er_max': 0.35} | -0.763 | -0.242 | 216 | -0.989 | -0.212 | -0.024 | 0.343 |
| {'lookback': 48, 'z_in': 2.0, 'k_atr': 3.0, 'er_max': 0.35} | -0.768 | -0.365 | 708 | -0.760 | -0.785 | -0.132 | 0.467 |
| {'lookback': 96, 'z_in': 3.0, 'k_atr': 3.0, 'er_max': 1.01} | -0.773 | -0.245 | 165 | -0.761 | -0.954 | -0.095 | 0.325 |
| {'lookback': 48, 'z_in': 2.5, 'k_atr': 2.0, 'er_max': 0.35} | -0.959 | -0.443 | 440 | -0.971 | -0.932 | -0.162 | 0.536 |

_36 configurations in total; top 10 by research Sharpe shown. Median research Sharpe -1.09._

### Walk-forward (re-optimised each window; out-of-sample test spans)

| test_start | test_end | params | train_sharpe | oos_return | oos_sharpe | oos_trades | oos_mdd |
|---|---|---|---|---|---|---|---|
| 2020-09-30 00:00:00+00:00 | 2020-12-28 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 48, 'z_in': 3.0} | 0.691 | -0.100 | -4.902 | 14 | 0.103 |
| 2020-12-29 00:00:00+00:00 | 2021-03-28 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 2.0} | -0.537 | -0.064 | -1.811 | 61 | 0.145 |
| 2021-03-29 00:00:00+00:00 | 2021-06-26 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 2.0} | -0.865 | 0.008 | 0.234 | 53 | 0.072 |
| 2021-06-27 00:00:00+00:00 | 2021-09-24 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 0.602 | 0.026 | 4.148 | 4 | 0.011 |
| 2021-09-25 00:00:00+00:00 | 2021-12-23 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 0.972 | -0.002 | -0.141 | 6 | 0.017 |
| 2021-12-24 00:00:00+00:00 | 2022-03-23 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 1.390 | 0.029 | 2.354 | 11 | 0.021 |
| 2022-03-24 00:00:00+00:00 | 2022-06-21 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 1.950 | 0.004 | 0.276 | 10 | 0.030 |
| 2022-06-22 00:00:00+00:00 | 2022-09-19 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 1.290 | -0.016 | -1.615 | 9 | 0.042 |
| 2022-09-20 00:00:00+00:00 | 2022-12-18 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 96, 'z_in': 3.0} | -0.195 | -0.083 | -5.561 | 8 | 0.088 |
| 2022-12-19 00:00:00+00:00 | 2023-03-18 23:00:00+00:00 | {'er_max': 1.01, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 0.350 | -0.016 | -1.068 | 10 | 0.038 |
| 2023-03-19 00:00:00+00:00 | 2023-06-16 23:00:00+00:00 | {'er_max': 1.01, 'k_atr': 2.0, 'lookback': 96, 'z_in': 2.5} | -0.018 | -0.005 | -0.014 | 17 | 0.057 |
| 2023-06-17 00:00:00+00:00 | 2023-09-14 23:00:00+00:00 | {'er_max': 1.01, 'k_atr': 2.0, 'lookback': 96, 'z_in': 2.0} | -1.191 | -0.068 | -2.197 | 21 | 0.099 |
| 2023-09-15 00:00:00+00:00 | 2023-12-13 23:00:00+00:00 | {'er_max': 1.01, 'k_atr': 2.0, 'lookback': 96, 'z_in': 2.0} | -1.373 | 0.019 | 0.778 | 19 | 0.060 |
| 2023-12-14 00:00:00+00:00 | 2024-03-12 23:00:00+00:00 | {'er_max': 1.01, 'k_atr': 2.0, 'lookback': 96, 'z_in': 2.5} | 0.077 | -0.030 | -1.103 | 15 | 0.064 |
| 2024-03-13 00:00:00+00:00 | 2024-06-10 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 96, 'z_in': 3.0} | -0.434 | 0.030 | 1.260 | 9 | 0.044 |

![wfo](research_wfo.png)

### Parameter sensitivity (chosen config vs one-step neighbours, research period)

| role | params | sharpe | ret | n_trades |
|---|---|---|---|---|
| chosen | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 0.025 | -0.000 | 163 |
| neighbour | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 48, 'z_in': 3.0} | -0.763 | -0.242 | 216 |
| neighbour | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 2.5} | -1.801 | -0.561 | 561 |
| neighbour | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 24, 'z_in': 3.0} | -0.164 | -0.068 | 161 |
| neighbour | {'er_max': 1.01, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | -0.367 | -0.125 | 258 |

## Family `squeeze`

### Research grid (every configuration tried; all count as trials)

| params | research_sharpe | research_ret | research_trades | train_sharpe | val_sharpe | val_ret | research_mdd |
|---|---|---|---|---|---|---|---|
| {'lookback': 24, 'quantile': 0.2, 'k_atr': 4.0} | 0.886 | 0.616 | 848 | 1.152 | 0.307 | 0.046 | 0.176 |
| {'lookback': 48, 'quantile': 0.1, 'k_atr': 4.0} | 0.509 | 0.221 | 323 | 0.878 | -0.372 | -0.051 | 0.144 |
| {'lookback': 24, 'quantile': 0.1, 'k_atr': 4.0} | 0.508 | 0.226 | 565 | 0.761 | -0.106 | -0.019 | 0.198 |
| {'lookback': 24, 'quantile': 0.2, 'k_atr': 3.0} | 0.505 | 0.362 | 845 | 0.586 | 0.306 | 0.053 | 0.268 |
| {'lookback': 24, 'quantile': 0.2, 'k_atr': 2.0} | 0.328 | 0.232 | 831 | 0.281 | 0.439 | 0.099 | 0.291 |
| {'lookback': 48, 'quantile': 0.1, 'k_atr': 3.0} | 0.314 | 0.138 | 322 | 0.330 | 0.280 | 0.037 | 0.208 |
| {'lookback': 24, 'quantile': 0.1, 'k_atr': 3.0} | 0.294 | 0.140 | 567 | 0.445 | -0.075 | -0.020 | 0.246 |
| {'lookback': 48, 'quantile': 0.2, 'k_atr': 4.0} | 0.294 | 0.129 | 452 | 1.029 | -1.597 | -0.208 | 0.250 |
| {'lookback': 48, 'quantile': 0.2, 'k_atr': 3.0} | 0.117 | 0.033 | 451 | 0.545 | -0.861 | -0.149 | 0.233 |
| {'lookback': 24, 'quantile': 0.1, 'k_atr': 2.0} | 0.029 | -0.028 | 556 | 0.152 | -0.280 | -0.065 | 0.312 |

_12 configurations in total; top 10 by research Sharpe shown. Median research Sharpe 0.30._

### Walk-forward (re-optimised each window; out-of-sample test spans)

| test_start | test_end | params | train_sharpe | oos_return | oos_sharpe | oos_trades | oos_mdd |
|---|---|---|---|---|---|---|---|
| 2020-09-30 00:00:00+00:00 | 2020-12-28 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2} | -0.272 | 0.113 | 2.988 | 25 | 0.044 |
| 2020-12-29 00:00:00+00:00 | 2021-03-28 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2} | 0.678 | 0.158 | 5.063 | 22 | 0.023 |
| 2021-03-29 00:00:00+00:00 | 2021-06-26 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2} | 1.634 | 0.012 | 0.489 | 27 | 0.046 |
| 2021-06-27 00:00:00+00:00 | 2021-09-24 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2} | 2.051 | 0.149 | 4.179 | 22 | 0.028 |
| 2021-09-25 00:00:00+00:00 | 2021-12-23 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 2.690 | 0.053 | 1.409 | 53 | 0.049 |
| 2021-12-24 00:00:00+00:00 | 2022-03-23 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 2.376 | -0.042 | -1.735 | 43 | 0.074 |
| 2022-03-24 00:00:00+00:00 | 2022-06-21 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 1.657 | 0.017 | 0.733 | 37 | 0.046 |
| 2022-06-22 00:00:00+00:00 | 2022-09-19 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.1} | 2.004 | -0.019 | -0.988 | 24 | 0.065 |
| 2022-09-20 00:00:00+00:00 | 2022-12-18 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 0.876 | 0.080 | 2.348 | 45 | 0.049 |
| 2022-12-19 00:00:00+00:00 | 2023-03-18 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 1.123 | 0.066 | 1.952 | 46 | 0.056 |
| 2023-03-19 00:00:00+00:00 | 2023-06-16 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 1.905 | -0.006 | -0.193 | 48 | 0.075 |
| 2023-06-17 00:00:00+00:00 | 2023-09-14 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 1.631 | 0.002 | 0.116 | 47 | 0.041 |
| 2023-09-15 00:00:00+00:00 | 2023-12-13 23:00:00+00:00 | {'k_atr': 3.0, 'lookback': 24, 'quantile': 0.2} | 1.311 | 0.001 | 0.086 | 40 | 0.063 |
| 2023-12-14 00:00:00+00:00 | 2024-03-12 23:00:00+00:00 | {'k_atr': 3.0, 'lookback': 24, 'quantile': 0.2} | 0.660 | 0.014 | 0.426 | 47 | 0.068 |
| 2024-03-13 00:00:00+00:00 | 2024-06-10 23:00:00+00:00 | {'k_atr': 3.0, 'lookback': 24, 'quantile': 0.1} | -0.002 | -0.020 | -0.647 | 31 | 0.057 |

![wfo](research_wfo.png)

### Parameter sensitivity (chosen config vs one-step neighbours, research period)

| role | params | sharpe | ret | n_trades |
|---|---|---|---|---|
| chosen | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.1} | 0.508 | 0.226 | 565 |
| neighbour | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.1} | 0.509 | 0.221 | 323 |
| neighbour | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 0.886 | 0.616 | 848 |
| neighbour | {'k_atr': 3.0, 'lookback': 24, 'quantile': 0.1} | 0.294 | 0.140 | 567 |

### HOLD-OUT result (single look, frozen parameters, net of costs)

Frozen params: `{'k_atr': 4.0, 'lookback': 24, 'quantile': 0.1}`  |  period 2024-07-01 → 2026-09-28 (2.245 y)  |  buy&hold over the same span: -97.7%

| metric | 1.0x costs | 1.5x costs |
|---|---|---|
| net_return | 0.314 | 0.217 |
| cagr | 0.129 | 0.092 |
| sharpe | 1.366 | 0.987 |
| sortino | 2.680 | 1.852 |
| max_drawdown | 0.069 | 0.075 |
| calmar | 1.873 | 1.224 |
| profit_factor | 1.410 | 1.274 |
| win_rate | 0.355 | 0.331 |
| n_trades | 251.000 | 251.000 |
| avg_r | 0.114 | 0.083 |
| avg_bars_held | 17.143 | 17.143 |
| ann_vol | 0.092 | 0.093 |
| fees_paid_pct | 0.108 | 0.156 |
| funding_paid_pct | -0.002 | -0.002 |
| stop_exits | 41.000 | 41.000 |
| kill_events | 0.000 | 0.000 |
| daily_halts | 0.000 | 0.000 |

### Acceptance criteria

| criterion | value | threshold | pass | detail |
|---|---|---|---|---|
| net return > 0 | 0.314 | > 0 | PASS |  |
| Sharpe | 1.366 | >= 1.0 | PASS |  |
| Sortino | 2.680 | >= 1.5 | PASS |  |
| Max drawdown | 0.069 | <= 0.2 | PASS |  |
| Profit factor | 1.410 | >= 1.3 | PASS |  |
| Trade count | 251.000 | >= 200 | PASS |  |
| Positive 90d windows | 0.700 | > 0.5 | PASS | 10 windows |
| Robust to 1.5x fees+slippage | 0.987 | Sharpe/Sortino/MDD/PF/net all still pass | FAIL | stressed: net=0.217 sharpe=0.99 sortino=1.85 mdd=0.075 pf=1.27 |
| Deflated Sharpe | 0.869 | >= 0.95 | FAIL | N_eff=8.5 (raw 80), SR0=0.67/yr; strict-variance DSR=0.001 (SR0=3.22/yr) |

**Verdict: NOT ACCEPTED**

### Multiple-testing correction
N_raw=80 configs tried, N_eff=8.5. Expected-max-Sharpe benchmark SR0=0.67/yr (null sampling variance); hold-out SR=1.37; DSR=0.869. Strict variant (empirical cross-trial variance, raw N): SR0=3.22/yr, DSR=0.001. Undeflated PSR(SR>0)=0.986; skew=2.11, kurtosis=12.7, n=820 days.

### Cost stress

| cost_multiplier | net_return | sharpe | sortino | max_drawdown | profit_factor | n_trades |
|---|---|---|---|---|---|---|
| 1.000 | 0.314 | 1.366 | 2.680 | 0.069 | 1.410 | 251.000 |
| 1.500 | 0.217 | 0.987 | 1.852 | 0.075 | 1.274 | 251.000 |
| 2.000 | 0.127 | 0.615 | 1.106 | 0.081 | 1.156 | 251.000 |

### Monte Carlo / bootstrap / placebo

* Trade-sequence MC (251 trades, resampled): P(profit)=0.961, final return p05/p50/p95 = +0.02/+0.31/+0.71, max-DD p50/p95/p99 = 0.08/0.15/0.18, P(MDD>20%)=0.005
* Stationary bootstrap of daily returns: Sharpe p05/p50/p95 = 0.28/1.37/2.48; P(Sharpe>0)=0.976
* Time-shift placebo (200 shifts): actual Sharpe 1.37 vs placebo mean -0.98 (p95 0.19); p-value 0.010
* 90-day windows positive: 0.70 of 10

### Hold-out by market regime (labels from trailing data only)

| dimension | regime | days | mean_daily_ret_bps | sharpe | total_return |
|---|---|---|---|---|---|
| trend | bear | 489 | 3.940 | 1.629 | 0.206 |
| trend | bull | 122 | 4.124 | 1.606 | 0.050 |
| trend | sideways | 209 | 1.907 | 0.694 | 0.038 |
| vol | high_vol | 484 | -1.642 | -0.748 | -0.080 |
| vol | low_vol | 336 | 10.783 | 3.722 | 0.429 |

### Same frozen parameters on other assets (hold-out span; NOT re-fit)

| asset | net_return | sharpe | max_drawdown | n_trades | profit_factor |
|---|---|---|---|---|---|
| ETH/USDT:USDT | 0.052 | 0.277 | 0.104 | 293.000 | 1.059 |
| BNB/USDT:USDT | 0.075 | 0.383 | 0.082 | 254.000 | 1.094 |
| XRP/USDT:USDT | -0.085 | -0.381 | 0.131 | 286.000 | 0.901 |
| LTC/USDT:USDT | 0.505 | 1.643 | 0.070 | 269.000 | 1.527 |
| ADA/USDT:USDT | 0.152 | 0.681 | 0.121 | 299.000 | 1.155 |

![holdout](holdout.png)

## Family `ml_gbm`

### Research grid (every configuration tried; all count as trials)

| params | research_sharpe | research_ret | research_trades | train_sharpe | val_sharpe | val_ret | research_mdd |
|---|---|---|---|---|---|---|---|
| {'horizon': 24, 'delta': 0.03, 'k_atr': 3.0} | 0.986 | 1.363 | 723 | 1.538 | -0.150 | -0.075 | 0.279 |
| {'horizon': 24, 'delta': 0.03, 'k_atr': 2.0} | 0.809 | 1.316 | 708 | 1.156 | 0.104 | -0.010 | 0.323 |
| {'horizon': 24, 'delta': 0.06, 'k_atr': 3.0} | 0.771 | 0.875 | 748 | 1.098 | 0.136 | 0.011 | 0.262 |
| {'horizon': 24, 'delta': 0.06, 'k_atr': 2.0} | 0.687 | 0.996 | 739 | 1.107 | -0.213 | -0.119 | 0.378 |
| {'horizon': 6, 'delta': 0.06, 'k_atr': 2.0} | 0.274 | 0.187 | 1424 | 0.071 | 0.699 | 0.213 | 0.385 |
| {'horizon': 6, 'delta': 0.06, 'k_atr': 3.0} | 0.126 | 0.037 | 1487 | 0.001 | 0.400 | 0.077 | 0.310 |
| {'horizon': 6, 'delta': 0.03, 'k_atr': 3.0} | 0.030 | -0.058 | 1883 | 0.301 | -0.525 | -0.170 | 0.378 |
| {'horizon': 6, 'delta': 0.03, 'k_atr': 2.0} | -0.190 | -0.323 | 1774 | -0.038 | -0.511 | -0.223 | 0.598 |

_8 configurations in total; top 10 by research Sharpe shown. Median research Sharpe 0.48._

### Walk-forward (re-optimised each window; out-of-sample test spans)

| test_start | test_end | params | train_sharpe | oos_return | oos_sharpe | oos_trades | oos_mdd |
|---|---|---|---|---|---|---|---|
| 2020-09-30 00:00:00+00:00 | 2020-12-28 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 2.0} | -0.065 | -0.034 | -0.444 | 57 | 0.134 |
| 2020-12-29 00:00:00+00:00 | 2021-03-28 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | -0.252 | 0.215 | 3.246 | 44 | 0.078 |
| 2021-03-29 00:00:00+00:00 | 2021-06-26 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | 0.740 | 0.070 | 1.092 | 48 | 0.124 |
| 2021-06-27 00:00:00+00:00 | 2021-09-24 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | 1.251 | 0.137 | 2.436 | 45 | 0.064 |
| 2021-09-25 00:00:00+00:00 | 2021-12-23 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | 1.734 | -0.020 | -0.365 | 46 | 0.123 |
| 2021-12-24 00:00:00+00:00 | 2022-03-23 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 2.0} | 1.384 | 0.011 | 0.231 | 48 | 0.096 |
| 2022-03-24 00:00:00+00:00 | 2022-06-21 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | 0.511 | -0.104 | -2.394 | 50 | 0.128 |
| 2022-06-22 00:00:00+00:00 | 2022-09-19 23:00:00+00:00 | {'delta': 0.03, 'horizon': 24, 'k_atr': 3.0} | 0.874 | 0.227 | 3.577 | 45 | 0.087 |
| 2022-09-20 00:00:00+00:00 | 2022-12-18 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | 0.059 | 0.394 | 6.393 | 37 | 0.057 |
| 2022-12-19 00:00:00+00:00 | 2023-03-18 23:00:00+00:00 | {'delta': 0.03, 'horizon': 24, 'k_atr': 3.0} | 3.175 | 0.024 | 0.573 | 36 | 0.138 |
| 2023-03-19 00:00:00+00:00 | 2023-06-16 23:00:00+00:00 | {'delta': 0.03, 'horizon': 24, 'k_atr': 2.0} | 3.089 | 0.004 | 0.231 | 47 | 0.123 |
| 2023-06-17 00:00:00+00:00 | 2023-09-14 23:00:00+00:00 | {'delta': 0.03, 'horizon': 24, 'k_atr': 3.0} | 2.624 | -0.061 | -1.087 | 41 | 0.131 |
| 2023-09-15 00:00:00+00:00 | 2023-12-13 23:00:00+00:00 | {'delta': 0.06, 'horizon': 6, 'k_atr': 3.0} | 2.042 | -0.002 | 0.005 | 73 | 0.067 |
| 2023-12-14 00:00:00+00:00 | 2024-03-12 23:00:00+00:00 | {'delta': 0.06, 'horizon': 6, 'k_atr': 3.0} | 0.722 | -0.048 | -0.976 | 85 | 0.127 |
| 2024-03-13 00:00:00+00:00 | 2024-06-10 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 2.0} | -0.603 | -0.070 | -1.315 | 43 | 0.180 |

![wfo](research_wfo.png)

### Parameter sensitivity (chosen config vs one-step neighbours, research period)

| role | params | sharpe | ret | n_trades |
|---|---|---|---|---|
| chosen | {'delta': 0.03, 'horizon': 24, 'k_atr': 3.0} | 0.986 | 1.363 | 723 |
| neighbour | {'delta': 0.03, 'horizon': 6, 'k_atr': 3.0} | 0.030 | -0.058 | 1883 |
| neighbour | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | 0.771 | 0.875 | 748 |
| neighbour | {'delta': 0.03, 'horizon': 24, 'k_atr': 2.0} | 0.809 | 1.316 | 708 |

### HOLD-OUT result (single look, frozen parameters, net of costs)

Frozen params: `{'delta': 0.03, 'horizon': 24, 'k_atr': 3.0}`  |  period 2024-07-01 → 2026-09-28 (2.245 y)  |  buy&hold over the same span: -97.7%

| metric | 1.0x costs | 1.5x costs |
|---|---|---|
| net_return | 0.386 | 0.209 |
| cagr | 0.156 | 0.088 |
| sharpe | 0.790 | 0.502 |
| sortino | 1.271 | 0.794 |
| max_drawdown | 0.160 | 0.172 |
| calmar | 0.978 | 0.514 |
| profit_factor | 1.146 | 1.081 |
| win_rate | 0.400 | 0.398 |
| n_trades | 400.000 | 400.000 |
| avg_r | 0.096 | 0.062 |
| avg_bars_held | 31.422 | 31.262 |
| ann_vol | 0.212 | 0.213 |
| fees_paid_pct | 0.196 | 0.276 |
| funding_paid_pct | -0.005 | -0.004 |
| stop_exits | 185.000 | 188.000 |
| kill_events | 1.000 | 1.000 |
| daily_halts | 4.000 | 4.000 |

### Acceptance criteria

| criterion | value | threshold | pass | detail |
|---|---|---|---|---|
| net return > 0 | 0.386 | > 0 | PASS |  |
| Sharpe | 0.790 | >= 1.0 | FAIL |  |
| Sortino | 1.271 | >= 1.5 | FAIL |  |
| Max drawdown | 0.160 | <= 0.2 | PASS |  |
| Profit factor | 1.146 | >= 1.3 | FAIL |  |
| Trade count | 400.000 | >= 200 | PASS |  |
| Positive 90d windows | 0.700 | > 0.5 | PASS | 10 windows |
| Robust to 1.5x fees+slippage | 0.502 | Sharpe/Sortino/MDD/PF/net all still pass | FAIL | stressed: net=0.209 sharpe=0.50 sortino=0.79 mdd=0.172 pf=1.08 |
| Deflated Sharpe | 0.573 | >= 0.95 | FAIL | N_eff=8.5 (raw 80), SR0=0.67/yr; strict-variance DSR=0.000 (SR0=3.22/yr) |

**Verdict: NOT ACCEPTED**

### Multiple-testing correction
N_raw=80 configs tried, N_eff=8.5. Expected-max-Sharpe benchmark SR0=0.67/yr (null sampling variance); hold-out SR=0.79; DSR=0.573. Strict variant (empirical cross-trial variance, raw N): SR0=3.22/yr, DSR=0.000. Undeflated PSR(SR>0)=0.885; skew=0.69, kurtosis=7.3, n=820 days.

### Cost stress

| cost_multiplier | net_return | sharpe | sortino | max_drawdown | profit_factor | n_trades |
|---|---|---|---|---|---|---|
| 1.000 | 0.386 | 0.790 | 1.271 | 0.160 | 1.146 | 400.000 |
| 1.500 | 0.209 | 0.502 | 0.794 | 0.172 | 1.081 | 400.000 |
| 2.000 | -0.073 | -0.054 | -0.082 | 0.200 | 0.968 | 402.000 |

### Monte Carlo / bootstrap / placebo

* Trade-sequence MC (400 trades, resampled): P(profit)=0.827, final return p05/p50/p95 = -0.19/+0.38/+1.44, max-DD p50/p95/p99 = 0.22/0.39/0.46, P(MDD>20%)=0.620
* Stationary bootstrap of daily returns: Sharpe p05/p50/p95 = -0.27/0.78/1.84; P(Sharpe>0)=0.893
* Time-shift placebo (200 shifts): actual Sharpe 0.79 vs placebo mean -0.25 (p95 1.00); p-value 0.075
* 90-day windows positive: 0.70 of 10

### Hold-out by market regime (labels from trailing data only)

| dimension | regime | days | mean_daily_ret_bps | sharpe | total_return |
|---|---|---|---|---|---|
| trend | bear | 489 | 3.165 | 0.586 | 0.137 |
| trend | bull | 122 | 6.535 | 0.999 | 0.073 |
| trend | sideways | 209 | 6.765 | 1.083 | 0.135 |
| vol | high_vol | 484 | 3.812 | 0.722 | 0.173 |
| vol | low_vol | 336 | 5.696 | 0.879 | 0.180 |

### Same frozen parameters on other assets (hold-out span; NOT re-fit)

| asset | net_return | sharpe | max_drawdown | n_trades | profit_factor |
|---|---|---|---|---|---|
| ETH/USDT:USDT | 0.577 | 1.059 | 0.203 | 377.000 | 1.236 |
| BNB/USDT:USDT | 0.177 | 0.461 | 0.231 | 421.000 | 1.074 |
| XRP/USDT:USDT | 0.658 | 1.222 | 0.234 | 297.000 | 1.245 |
| LTC/USDT:USDT | 0.790 | 1.355 | 0.190 | 339.000 | 1.317 |
| ADA/USDT:USDT | 0.091 | 0.296 | 0.203 | 345.000 | 1.047 |

![holdout](holdout.png)
