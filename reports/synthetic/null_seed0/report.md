# SYNTHETIC null market (seed 0) — pipeline validation, NOT evidence of an edge

> Synthetic data. Demonstrates the pipeline's behaviour; says nothing about real markets.

Trials registered: **80** configurations (effective independent ≈ 9.1); by family: {'donchian': 24, 'meanrev': 36, 'squeeze': 12, 'ml_gbm': 8}

## Summary

| family | stage | params | net | sharpe | sortino | mdd | PF | trades | DSR | accepted |
|---|---|---|---|---|---|---|---|---|---|---|
| donchian | rejected at research | {'allow_short': True, 'k_atr': 3.0, 'n': 96} | None | None | None | None | None | None | None | no |
| meanrev | rejected at research | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 48, 'z_in': 3.0} | None | None | None | None | None | None | None | no |
| squeeze | rejected at research | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.1} | None | None | None | None | None | None | None | no |
| ml_gbm | rejected at research | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | None | None | None | None | None | None | None | no |

## Family `donchian`

### Research gates (train+validation only)

| gate | value | threshold | pass |
|---|---|---|---|
| wfo_sharpe | -0.032 | 0.800 | no |
| wfo_positive_windows | 0.333 | 0.500 | no |
| research_trades | 306.000 | 100.000 | yes |
| sensitivity_neighbours_positive | 0.600 | 0.600 | yes |

### Research grid (every configuration tried; all count as trials)

| params | research_sharpe | research_ret | research_trades | train_sharpe | val_sharpe | val_ret | research_mdd |
|---|---|---|---|---|---|---|---|
| {'n': 96, 'k_atr': 3.0, 'allow_short': True} | 0.689 | 0.637 | 306 | 1.040 | -0.194 | -0.063 | 0.283 |
| {'n': 96, 'k_atr': 4.0, 'allow_short': True} | 0.510 | 0.353 | 309 | 0.939 | -0.661 | -0.132 | 0.283 |
| {'n': 96, 'k_atr': 2.0, 'allow_short': True} | 0.498 | 0.488 | 305 | 0.950 | -0.675 | -0.199 | 0.338 |
| {'n': 48, 'k_atr': 4.0, 'allow_short': True} | 0.393 | 0.260 | 550 | 1.013 | -1.137 | -0.230 | 0.298 |
| {'n': 48, 'k_atr': 3.0, 'allow_short': True} | 0.113 | 0.018 | 551 | 0.810 | -1.372 | -0.326 | 0.426 |
| {'n': 48, 'k_atr': 2.0, 'allow_short': True} | 0.105 | -0.018 | 540 | 0.628 | -1.132 | -0.355 | 0.477 |
| {'n': 96, 'k_atr': 3.0, 'allow_short': False} | -0.027 | -0.049 | 149 | -0.141 | 0.435 | 0.071 | 0.321 |
| {'n': 192, 'k_atr': 3.0, 'allow_short': True} | -0.029 | -0.065 | 176 | 0.241 | -0.805 | -0.148 | 0.258 |
| {'n': 24, 'k_atr': 4.0, 'allow_short': True} | -0.058 | -0.097 | 1024 | 0.121 | -0.539 | -0.121 | 0.251 |
| {'n': 48, 'k_atr': 3.0, 'allow_short': False} | -0.167 | -0.144 | 286 | 0.109 | -1.158 | -0.217 | 0.320 |

_24 configurations in total; top 10 by research Sharpe shown. Median research Sharpe -0.22._

### Walk-forward (re-optimised each window; out-of-sample test spans)

| test_start | test_end | params | train_sharpe | oos_return | oos_sharpe | oos_trades | oos_mdd |
|---|---|---|---|---|---|---|---|
| 2020-09-30 00:00:00+00:00 | 2020-12-28 23:00:00+00:00 | {'allow_short': False, 'k_atr': 2.0, 'n': 96} | 0.764 | -0.027 | -0.603 | 9 | 0.082 |
| 2020-12-29 00:00:00+00:00 | 2021-03-28 23:00:00+00:00 | {'allow_short': False, 'k_atr': 2.0, 'n': 48} | 0.322 | 0.066 | 1.479 | 15 | 0.062 |
| 2021-03-29 00:00:00+00:00 | 2021-06-26 23:00:00+00:00 | {'allow_short': False, 'k_atr': 2.0, 'n': 24} | 0.325 | -0.025 | -0.264 | 32 | 0.099 |
| 2021-06-27 00:00:00+00:00 | 2021-09-24 23:00:00+00:00 | {'allow_short': False, 'k_atr': 2.0, 'n': 24} | 0.578 | -0.003 | 0.002 | 24 | 0.078 |
| 2021-09-25 00:00:00+00:00 | 2021-12-23 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 48} | 1.554 | -0.001 | 0.088 | 31 | 0.104 |
| 2021-12-24 00:00:00+00:00 | 2022-03-23 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 48} | 1.729 | 0.065 | 1.425 | 25 | 0.074 |
| 2022-03-24 00:00:00+00:00 | 2022-06-21 23:00:00+00:00 | {'allow_short': True, 'k_atr': 4.0, 'n': 96} | 1.951 | -0.118 | -3.531 | 19 | 0.130 |
| 2022-06-22 00:00:00+00:00 | 2022-09-19 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 48} | 0.946 | 0.336 | 5.282 | 24 | 0.049 |
| 2022-09-20 00:00:00+00:00 | 2022-12-18 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 48} | 1.210 | 0.021 | 0.546 | 25 | 0.086 |
| 2022-12-19 00:00:00+00:00 | 2023-03-18 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 96} | 1.712 | -0.115 | -3.173 | 19 | 0.129 |
| 2023-03-19 00:00:00+00:00 | 2023-06-16 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 96} | 0.050 | 0.000 | 0.091 | 16 | 0.091 |
| 2023-06-17 00:00:00+00:00 | 2023-09-14 23:00:00+00:00 | {'allow_short': True, 'k_atr': 3.0, 'n': 96} | 1.289 | -0.113 | -3.255 | 21 | 0.134 |
| 2023-09-15 00:00:00+00:00 | 2023-12-13 23:00:00+00:00 | {'allow_short': False, 'k_atr': 3.0, 'n': 192} | -0.005 | -0.020 | -0.862 | 5 | 0.070 |
| 2023-12-14 00:00:00+00:00 | 2024-03-12 23:00:00+00:00 | {'allow_short': True, 'k_atr': 4.0, 'n': 24} | -0.490 | -0.027 | -0.588 | 58 | 0.108 |
| 2024-03-13 00:00:00+00:00 | 2024-06-10 23:00:00+00:00 | {'allow_short': True, 'k_atr': 4.0, 'n': 24} | 0.129 | -0.040 | -1.082 | 57 | 0.087 |

![wfo](research_wfo.png)

### Parameter sensitivity (chosen config vs one-step neighbours, research period)

| role | params | sharpe | ret | n_trades |
|---|---|---|---|---|
| chosen | {'allow_short': True, 'k_atr': 3.0, 'n': 96} | 0.689 | 0.637 | 306 |
| neighbour | {'allow_short': True, 'k_atr': 3.0, 'n': 48} | 0.113 | 0.018 | 551 |
| neighbour | {'allow_short': True, 'k_atr': 3.0, 'n': 192} | -0.029 | -0.065 | 176 |
| neighbour | {'allow_short': True, 'k_atr': 2.0, 'n': 96} | 0.498 | 0.488 | 305 |
| neighbour | {'allow_short': True, 'k_atr': 4.0, 'n': 96} | 0.510 | 0.353 | 309 |
| neighbour | {'allow_short': False, 'k_atr': 3.0, 'n': 96} | -0.027 | -0.049 | 149 |

## Family `meanrev`

### Research gates (train+validation only)

| gate | value | threshold | pass |
|---|---|---|---|
| wfo_sharpe | -0.793 | 0.800 | no |
| wfo_positive_windows | 0.267 | 0.500 | no |
| research_trades | 221.000 | 100.000 | yes |
| sensitivity_neighbours_positive | 0.000 | 0.600 | no |

### Research grid (every configuration tried; all count as trials)

| params | research_sharpe | research_ret | research_trades | train_sharpe | val_sharpe | val_ret | research_mdd |
|---|---|---|---|---|---|---|---|
| {'lookback': 48, 'z_in': 2.0, 'k_atr': 2.0, 'er_max': 0.35} | -0.389 | -0.296 | 734 | -0.690 | 0.281 | 0.049 | 0.423 |
| {'lookback': 48, 'z_in': 2.0, 'k_atr': 2.0, 'er_max': 1.01} | -0.407 | -0.306 | 726 | -0.714 | 0.278 | 0.048 | 0.446 |
| {'lookback': 96, 'z_in': 3.0, 'k_atr': 2.0, 'er_max': 0.35} | -0.408 | -0.178 | 172 | -1.103 | 0.955 | 0.141 | 0.326 |
| {'lookback': 96, 'z_in': 3.0, 'k_atr': 2.0, 'er_max': 1.01} | -0.408 | -0.178 | 172 | -1.103 | 0.955 | 0.141 | 0.326 |
| {'lookback': 24, 'z_in': 3.0, 'k_atr': 3.0, 'er_max': 1.01} | -0.428 | -0.147 | 276 | -0.301 | -1.043 | -0.103 | 0.216 |
| {'lookback': 24, 'z_in': 3.0, 'k_atr': 3.0, 'er_max': 0.35} | -0.492 | -0.131 | 185 | -0.329 | -0.848 | -0.067 | 0.193 |
| {'lookback': 24, 'z_in': 3.0, 'k_atr': 2.0, 'er_max': 1.01} | -0.505 | -0.222 | 275 | -0.257 | -1.312 | -0.156 | 0.296 |
| {'lookback': 48, 'z_in': 2.5, 'k_atr': 3.0, 'er_max': 0.35} | -0.558 | -0.254 | 460 | -0.773 | -0.225 | -0.040 | 0.331 |
| {'lookback': 48, 'z_in': 2.0, 'k_atr': 3.0, 'er_max': 0.35} | -0.563 | -0.306 | 742 | -0.947 | 0.274 | 0.040 | 0.395 |
| {'lookback': 48, 'z_in': 2.0, 'k_atr': 3.0, 'er_max': 1.01} | -0.587 | -0.316 | 744 | -0.980 | 0.272 | 0.039 | 0.404 |

_36 configurations in total; top 10 by research Sharpe shown. Median research Sharpe -0.82._

### Walk-forward (re-optimised each window; out-of-sample test spans)

| test_start | test_end | params | train_sharpe | oos_return | oos_sharpe | oos_trades | oos_mdd |
|---|---|---|---|---|---|---|---|
| 2020-09-30 00:00:00+00:00 | 2020-12-28 23:00:00+00:00 | {'er_max': 1.01, 'k_atr': 2.0, 'lookback': 96, 'z_in': 2.0} | 0.120 | -0.038 | -1.267 | 20 | 0.064 |
| 2020-12-29 00:00:00+00:00 | 2021-03-28 23:00:00+00:00 | {'er_max': 1.01, 'k_atr': 2.0, 'lookback': 96, 'z_in': 2.0} | -0.366 | -0.008 | -0.203 | 21 | 0.049 |
| 2021-03-29 00:00:00+00:00 | 2021-06-26 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 48, 'z_in': 2.0} | -1.291 | -0.034 | -0.859 | 41 | 0.070 |
| 2021-06-27 00:00:00+00:00 | 2021-09-24 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 2.5} | -0.103 | -0.085 | -4.585 | 27 | 0.097 |
| 2021-09-25 00:00:00+00:00 | 2021-12-23 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 0.277 | 0.030 | 1.228 | 8 | 0.021 |
| 2021-12-24 00:00:00+00:00 | 2022-03-23 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 0.927 | -0.035 | -2.147 | 14 | 0.050 |
| 2022-03-24 00:00:00+00:00 | 2022-06-21 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 0.471 | 0.030 | 1.786 | 11 | 0.021 |
| 2022-06-22 00:00:00+00:00 | 2022-09-19 23:00:00+00:00 | {'er_max': 1.01, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0} | 1.580 | -0.029 | -2.664 | 11 | 0.034 |
| 2022-09-20 00:00:00+00:00 | 2022-12-18 23:00:00+00:00 | {'er_max': 1.01, 'k_atr': 2.0, 'lookback': 48, 'z_in': 3.0} | -0.020 | -0.017 | -0.752 | 13 | 0.040 |
| 2022-12-19 00:00:00+00:00 | 2023-03-18 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 48, 'z_in': 2.0} | 0.190 | 0.023 | 0.634 | 44 | 0.084 |
| 2023-03-19 00:00:00+00:00 | 2023-06-16 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 48, 'z_in': 3.0} | 0.226 | -0.071 | -4.720 | 9 | 0.081 |
| 2023-06-17 00:00:00+00:00 | 2023-09-14 23:00:00+00:00 | {'er_max': 1.01, 'k_atr': 2.0, 'lookback': 48, 'z_in': 2.0} | -0.481 | -0.081 | -2.421 | 38 | 0.121 |
| 2023-09-15 00:00:00+00:00 | 2023-12-13 23:00:00+00:00 | {'er_max': 1.01, 'k_atr': 3.0, 'lookback': 96, 'z_in': 3.0} | -0.399 | 0.063 | 3.231 | 9 | 0.019 |
| 2023-12-14 00:00:00+00:00 | 2024-03-12 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 96, 'z_in': 3.0} | 1.207 | -0.006 | -0.351 | 8 | 0.032 |
| 2024-03-13 00:00:00+00:00 | 2024-06-10 23:00:00+00:00 | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 96, 'z_in': 3.0} | 0.885 | -0.042 | -2.215 | 10 | 0.046 |

![wfo](research_wfo.png)

### Parameter sensitivity (chosen config vs one-step neighbours, research period)

| role | params | sharpe | ret | n_trades |
|---|---|---|---|---|
| chosen | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 48, 'z_in': 3.0} | -0.686 | -0.285 | 221 |
| neighbour | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 24, 'z_in': 3.0} | -0.726 | -0.240 | 186 |
| neighbour | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 96, 'z_in': 3.0} | -0.408 | -0.178 | 172 |
| neighbour | {'er_max': 0.35, 'k_atr': 2.0, 'lookback': 48, 'z_in': 2.5} | -0.655 | -0.357 | 455 |
| neighbour | {'er_max': 0.35, 'k_atr': 3.0, 'lookback': 48, 'z_in': 3.0} | -0.719 | -0.237 | 225 |
| neighbour | {'er_max': 1.01, 'k_atr': 2.0, 'lookback': 48, 'z_in': 3.0} | -0.827 | -0.340 | 240 |

## Family `squeeze`

### Research gates (train+validation only)

| gate | value | threshold | pass |
|---|---|---|---|
| wfo_sharpe | -0.570 | 0.800 | no |
| wfo_positive_windows | 0.333 | 0.500 | no |
| research_trades | 324.000 | 100.000 | yes |
| sensitivity_neighbours_positive | 0.000 | 0.600 | no |

### Research grid (every configuration tried; all count as trials)

| params | research_sharpe | research_ret | research_trades | train_sharpe | val_sharpe | val_ret | research_mdd |
|---|---|---|---|---|---|---|---|
| {'lookback': 48, 'quantile': 0.1, 'k_atr': 4.0} | -0.161 | -0.081 | 324 | 0.235 | -1.248 | -0.145 | 0.224 |
| {'lookback': 48, 'quantile': 0.2, 'k_atr': 4.0} | -0.183 | -0.109 | 459 | 0.166 | -1.257 | -0.168 | 0.213 |
| {'lookback': 48, 'quantile': 0.1, 'k_atr': 3.0} | -0.483 | -0.220 | 323 | -0.528 | -0.424 | -0.072 | 0.305 |
| {'lookback': 24, 'quantile': 0.1, 'k_atr': 4.0} | -0.516 | -0.224 | 586 | -0.326 | -0.966 | -0.126 | 0.271 |
| {'lookback': 48, 'quantile': 0.2, 'k_atr': 3.0} | -0.680 | -0.327 | 453 | -0.624 | -0.906 | -0.148 | 0.378 |
| {'lookback': 48, 'quantile': 0.2, 'k_atr': 2.0} | -0.743 | -0.400 | 448 | -0.687 | -0.905 | -0.172 | 0.463 |
| {'lookback': 24, 'quantile': 0.2, 'k_atr': 4.0} | -0.861 | -0.379 | 823 | -0.538 | -1.633 | -0.228 | 0.396 |
| {'lookback': 48, 'quantile': 0.1, 'k_atr': 2.0} | -0.987 | -0.411 | 311 | -1.324 | -0.396 | -0.083 | 0.448 |
| {'lookback': 24, 'quantile': 0.1, 'k_atr': 3.0} | -1.052 | -0.445 | 578 | -1.203 | -0.721 | -0.121 | 0.462 |
| {'lookback': 24, 'quantile': 0.2, 'k_atr': 2.0} | -1.196 | -0.641 | 786 | -1.388 | -0.778 | -0.194 | 0.677 |

_12 configurations in total; top 10 by research Sharpe shown. Median research Sharpe -0.80._

### Walk-forward (re-optimised each window; out-of-sample test spans)

| test_start | test_end | params | train_sharpe | oos_return | oos_sharpe | oos_trades | oos_mdd |
|---|---|---|---|---|---|---|---|
| 2020-09-30 00:00:00+00:00 | 2020-12-28 23:00:00+00:00 | {'k_atr': 2.0, 'lookback': 48, 'quantile': 0.1} | -0.834 | -0.001 | 0.038 | 19 | 0.041 |
| 2020-12-29 00:00:00+00:00 | 2021-03-28 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.1} | 0.299 | 0.012 | 0.858 | 17 | 0.037 |
| 2021-03-29 00:00:00+00:00 | 2021-06-26 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.1} | 0.879 | -0.007 | -0.311 | 17 | 0.036 |
| 2021-06-27 00:00:00+00:00 | 2021-09-24 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.1} | 1.201 | 0.080 | 2.822 | 15 | 0.027 |
| 2021-09-25 00:00:00+00:00 | 2021-12-23 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.1} | 1.966 | -0.011 | -0.326 | 22 | 0.049 |
| 2021-12-24 00:00:00+00:00 | 2022-03-23 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.1} | 1.358 | 0.041 | 1.732 | 24 | 0.045 |
| 2022-03-24 00:00:00+00:00 | 2022-06-21 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.1} | 1.219 | -0.078 | -3.638 | 28 | 0.109 |
| 2022-06-22 00:00:00+00:00 | 2022-09-19 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2} | 0.701 | 0.043 | 1.445 | 47 | 0.049 |
| 2022-09-20 00:00:00+00:00 | 2022-12-18 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.1} | -0.154 | -0.086 | -4.115 | 37 | 0.103 |
| 2022-12-19 00:00:00+00:00 | 2023-03-18 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2} | -0.185 | -0.031 | -0.937 | 26 | 0.058 |
| 2023-03-19 00:00:00+00:00 | 2023-06-16 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.1} | -0.503 | -0.001 | 0.025 | 18 | 0.062 |
| 2023-06-17 00:00:00+00:00 | 2023-09-14 23:00:00+00:00 | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2} | 0.464 | -0.039 | -2.351 | 22 | 0.052 |
| 2023-09-15 00:00:00+00:00 | 2023-12-13 23:00:00+00:00 | {'k_atr': 2.0, 'lookback': 48, 'quantile': 0.2} | -0.058 | -0.086 | -3.592 | 26 | 0.125 |
| 2023-12-14 00:00:00+00:00 | 2024-03-12 23:00:00+00:00 | {'k_atr': 2.0, 'lookback': 48, 'quantile': 0.2} | -0.617 | 0.009 | 0.318 | 21 | 0.070 |
| 2024-03-13 00:00:00+00:00 | 2024-06-10 23:00:00+00:00 | {'k_atr': 2.0, 'lookback': 48, 'quantile': 0.2} | -0.555 | -0.067 | -2.828 | 26 | 0.086 |

![wfo](research_wfo.png)

### Parameter sensitivity (chosen config vs one-step neighbours, research period)

| role | params | sharpe | ret | n_trades |
|---|---|---|---|---|
| chosen | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.1} | -0.161 | -0.081 | 324 |
| neighbour | {'k_atr': 4.0, 'lookback': 24, 'quantile': 0.1} | -0.516 | -0.224 | 586 |
| neighbour | {'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2} | -0.183 | -0.109 | 459 |
| neighbour | {'k_atr': 3.0, 'lookback': 48, 'quantile': 0.1} | -0.483 | -0.220 | 323 |

## Family `ml_gbm`

### Research gates (train+validation only)

| gate | value | threshold | pass |
|---|---|---|---|
| wfo_sharpe | -0.507 | 0.800 | no |
| wfo_positive_windows | 0.333 | 0.500 | no |
| research_trades | 720.000 | 100.000 | yes |
| sensitivity_neighbours_positive | 0.000 | 0.600 | no |

### Research grid (every configuration tried; all count as trials)

| params | research_sharpe | research_ret | research_trades | train_sharpe | val_sharpe | val_ret | research_mdd |
|---|---|---|---|---|---|---|---|
| {'horizon': 24, 'delta': 0.03, 'k_atr': 2.0} | -0.644 | -0.529 | 757 | -0.805 | -0.325 | -0.132 | 0.591 |
| {'horizon': 24, 'delta': 0.06, 'k_atr': 2.0} | -0.811 | -0.601 | 712 | -0.536 | -1.508 | -0.417 | 0.642 |
| {'horizon': 24, 'delta': 0.06, 'k_atr': 3.0} | -0.819 | -0.503 | 720 | -0.729 | -1.476 | -0.321 | 0.552 |
| {'horizon': 24, 'delta': 0.03, 'k_atr': 3.0} | -0.902 | -0.549 | 781 | -1.284 | -0.033 | -0.031 | 0.625 |
| {'horizon': 6, 'delta': 0.06, 'k_atr': 3.0} | -1.418 | -0.568 | 1305 | -1.531 | -0.943 | -0.165 | 0.597 |
| {'horizon': 6, 'delta': 0.06, 'k_atr': 2.0} | -1.806 | -0.751 | 1226 | -2.121 | -1.081 | -0.244 | 0.768 |
| {'horizon': 6, 'delta': 0.03, 'k_atr': 3.0} | -1.876 | -0.786 | 2092 | -2.045 | -1.567 | -0.364 | 0.802 |
| {'horizon': 6, 'delta': 0.03, 'k_atr': 2.0} | -2.447 | -0.922 | 1913 | -2.871 | -1.295 | -0.404 | 0.926 |

_8 configurations in total; top 10 by research Sharpe shown. Median research Sharpe -1.16._

### Walk-forward (re-optimised each window; out-of-sample test spans)

| test_start | test_end | params | train_sharpe | oos_return | oos_sharpe | oos_trades | oos_mdd |
|---|---|---|---|---|---|---|---|
| 2020-09-30 00:00:00+00:00 | 2020-12-28 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 2.0} | -1.794 | -0.023 | -0.305 | 47 | 0.134 |
| 2020-12-29 00:00:00+00:00 | 2021-03-28 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 2.0} | -1.752 | -0.150 | -2.638 | 52 | 0.151 |
| 2021-03-29 00:00:00+00:00 | 2021-06-26 23:00:00+00:00 | {'delta': 0.03, 'horizon': 24, 'k_atr': 3.0} | -2.829 | -0.137 | -3.377 | 43 | 0.153 |
| 2021-06-27 00:00:00+00:00 | 2021-09-24 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 2.0} | -1.260 | 0.053 | 1.203 | 44 | 0.074 |
| 2021-09-25 00:00:00+00:00 | 2021-12-23 23:00:00+00:00 | {'delta': 0.03, 'horizon': 24, 'k_atr': 3.0} | -0.606 | -0.092 | -2.030 | 61 | 0.146 |
| 2021-12-24 00:00:00+00:00 | 2022-03-23 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 2.0} | -0.929 | -0.082 | -1.751 | 37 | 0.119 |
| 2022-03-24 00:00:00+00:00 | 2022-06-21 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 2.0} | -1.015 | -0.032 | -0.428 | 48 | 0.122 |
| 2022-06-22 00:00:00+00:00 | 2022-09-19 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 2.0} | -0.647 | 0.266 | 3.475 | 48 | 0.081 |
| 2022-09-20 00:00:00+00:00 | 2022-12-18 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | -0.086 | 0.042 | 0.950 | 47 | 0.079 |
| 2022-12-19 00:00:00+00:00 | 2023-03-18 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | 0.663 | -0.148 | -2.850 | 42 | 0.156 |
| 2023-03-19 00:00:00+00:00 | 2023-06-16 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | 0.331 | 0.072 | 1.750 | 44 | 0.100 |
| 2023-06-17 00:00:00+00:00 | 2023-09-14 23:00:00+00:00 | {'delta': 0.03, 'horizon': 24, 'k_atr': 3.0} | 0.299 | -0.066 | -1.613 | 46 | 0.132 |
| 2023-09-15 00:00:00+00:00 | 2023-12-13 23:00:00+00:00 | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | -0.211 | -0.042 | -1.159 | 43 | 0.103 |
| 2023-12-14 00:00:00+00:00 | 2024-03-12 23:00:00+00:00 | {'delta': 0.03, 'horizon': 24, 'k_atr': 3.0} | -0.449 | 0.073 | 1.580 | 46 | 0.080 |
| 2024-03-13 00:00:00+00:00 | 2024-06-10 23:00:00+00:00 | {'delta': 0.03, 'horizon': 24, 'k_atr': 3.0} | 0.854 | -0.102 | -2.834 | 58 | 0.122 |

![wfo](research_wfo.png)

### Parameter sensitivity (chosen config vs one-step neighbours, research period)

| role | params | sharpe | ret | n_trades |
|---|---|---|---|---|
| chosen | {'delta': 0.06, 'horizon': 24, 'k_atr': 3.0} | -0.819 | -0.503 | 720 |
| neighbour | {'delta': 0.06, 'horizon': 6, 'k_atr': 3.0} | -1.418 | -0.568 | 1305 |
| neighbour | {'delta': 0.03, 'horizon': 24, 'k_atr': 3.0} | -0.902 | -0.549 | 781 |
| neighbour | {'delta': 0.06, 'horizon': 24, 'k_atr': 2.0} | -0.811 | -0.601 | 712 |
