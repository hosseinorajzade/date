# Synthetic pipeline-validation summary

All data here is **synthetic**. A *null* market is an exact martingale (no edge exists); *planted* markets contain an Ornstein-Uhlenbeck drift (`weak` = 0.06, `moderate` = 0.12 × base vol per hour). Purpose: measure the false-positive rate and the power of the *pipeline*, not the profitability of anything.

## Per scenario

| scenario | runs | family_tests | passed_research_gates | accepted | gate_pass_rate | accept_rate |
|---|---|---|---|---|---|---|
| null | 12 | 48 | 0 | 0 | 0.000 | 0.000 |
| planted_moderate | 4 | 16 | 12 | 9 | 0.750 | 0.562 |
| planted_weak | 4 | 16 | 9 | 0 | 0.562 | 0.000 |

## Per scenario and family

| scenario | family | tests | reached_holdout | accepted | median_holdout_sharpe |
|---|---|---|---|---|---|
| null | donchian | 12 | 0 | 0 | n/a |
| null | meanrev | 12 | 0 | 0 | n/a |
| null | ml_gbm | 12 | 0 | 0 | n/a |
| null | squeeze | 12 | 0 | 0 | n/a |
| planted_moderate | donchian | 4 | 4 | 3 | 4.810 |
| planted_moderate | meanrev | 4 | 0 | 0 | n/a |
| planted_moderate | ml_gbm | 4 | 4 | 3 | 4.568 |
| planted_moderate | squeeze | 4 | 4 | 3 | 2.678 |
| planted_weak | donchian | 4 | 3 | 0 | 1.466 |
| planted_weak | meanrev | 4 | 0 | 0 | n/a |
| planted_weak | ml_gbm | 4 | 4 | 0 | 0.697 |
| planted_weak | squeeze | 4 | 2 | 0 | 0.764 |

## Every hold-out evaluation

| scenario | run | family | accepted | sharpe | mdd | pf | trades | dsr | dsr_strict | placebo_p | net_return |
|---|---|---|---|---|---|---|---|---|---|---|---|
| planted_moderate | planted_moderate_seed0 | donchian | yes | 5.036 | 0.125 | 3.222 | 224.000 | 1.000 | 0.002 | 0.010 | 7.275 |
| planted_moderate | planted_moderate_seed0 | ml_gbm | yes | 4.688 | 0.109 | 2.694 | 317.000 | 1.000 | 0.000 | 0.010 | 10.772 |
| planted_moderate | planted_moderate_seed0 | squeeze | yes | 2.884 | 0.109 | 1.819 | 360.000 | 1.000 | 0.000 | 0.010 | 1.249 |
| planted_moderate | planted_moderate_seed1 | donchian | yes | 4.822 | 0.125 | 2.458 | 239.000 | 1.000 | 0.000 | 0.010 | 7.114 |
| planted_moderate | planted_moderate_seed1 | ml_gbm | no | 4.635 | 0.222 | 2.250 | 267.000 | 1.000 | 0.000 | 0.010 | 11.885 |
| planted_moderate | planted_moderate_seed1 | squeeze | yes | 2.610 | 0.087 | 1.963 | 208.000 | 1.000 | 0.000 | 0.010 | 1.088 |
| planted_moderate | planted_moderate_seed2 | donchian | yes | 4.798 | 0.118 | 3.030 | 225.000 | 1.000 | 0.000 | 0.010 | 7.834 |
| planted_moderate | planted_moderate_seed2 | ml_gbm | yes | 4.501 | 0.156 | 1.815 | 625.000 | 1.000 | 0.000 | 0.010 | 7.877 |
| planted_moderate | planted_moderate_seed2 | squeeze | no | 2.747 | 0.095 | 2.139 | 196.000 | 1.000 | 0.000 | 0.010 | 1.044 |
| planted_moderate | planted_moderate_seed3 | donchian | no | 4.522 | 0.072 | 3.090 | 110.000 | 1.000 | 0.001 | 0.010 | 3.403 |
| planted_moderate | planted_moderate_seed3 | ml_gbm | yes | 4.472 | 0.111 | 1.866 | 684.000 | 1.000 | 0.001 | 0.010 | 6.572 |
| planted_moderate | planted_moderate_seed3 | squeeze | yes | 2.380 | 0.115 | 1.969 | 208.000 | 0.998 | 0.000 | 0.010 | 0.958 |
| planted_weak | planted_weak_seed0 | donchian | no | 1.584 | 0.143 | 1.685 | 144.000 | 0.921 | 0.006 | 0.025 | 0.726 |
| planted_weak | planted_weak_seed0 | ml_gbm | no | 0.790 | 0.160 | 1.146 | 400.000 | 0.573 | 0.000 | 0.075 | 0.386 |
| planted_weak | planted_weak_seed0 | squeeze | no | 1.366 | 0.069 | 1.410 | 251.000 | 0.869 | 0.001 | 0.010 | 0.314 |
| planted_weak | planted_weak_seed1 | donchian | no | 1.466 | 0.165 | 1.714 | 80.000 | 0.881 | 0.010 | 0.080 | 0.640 |
| planted_weak | planted_weak_seed1 | ml_gbm | no | 1.082 | 0.208 | 1.220 | 358.000 | 0.722 | 0.002 | 0.040 | 0.524 |
| planted_weak | planted_weak_seed1 | squeeze | no | 0.163 | 0.212 | 1.031 | 230.000 | 0.210 | 0.000 | 0.184 | 0.027 |
| planted_weak | planted_weak_seed2 | donchian | no | 0.499 | 0.117 | 1.241 | 72.000 | 0.399 | 0.000 | 0.318 | 0.132 |
| planted_weak | planted_weak_seed2 | ml_gbm | no | -0.526 | 0.312 | 0.876 | 305.000 | 0.037 | 0.000 | 0.811 | -0.222 |
| planted_weak | planted_weak_seed3 | ml_gbm | no | 0.604 | 0.225 | 1.114 | 370.000 | 0.443 | 0.001 | 0.075 | 0.237 |
