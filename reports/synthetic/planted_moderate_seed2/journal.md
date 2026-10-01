

### [synthetic-planted-seed2] research: donchian
*2026-10-01 10:56Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': True, 'k_atr': 4.0, 'n': 48}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 1.0, "oos_sharpe": 5.79762030717115, "oos_sortino": 14.239279613048119, "oos_mdd": 0.10175782006339062, "oos_net_return": 130.79911472322107, "oos_trades": 239, "oos_profit_factor": 5.9540385510847464, "distinct_param_sets_chosen": 6, "median_train_sharpe": 6.60796243741726}

gates: {"wfo_sharpe": [5.79762030717115, 0.8, true], "wfo_positive_windows": [1.0, 0.5, true], "research_trades": [460.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed2] research: meanrev
*2026-10-01 10:56Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 2.0, 'lookback': 96, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4, "oos_sharpe": -0.5684643092043493, "oos_sortino": -0.8233747448913259, "oos_mdd": 0.22539168816267685, "oos_net_return": -0.14984110997598998, "oos_trades": 123, "oos_profit_factor": 0.8093690388407465, "distinct_param_sets_chosen": 4, "median_train_sharpe": -0.3026216274867812}

gates: {"wfo_sharpe": [-0.5684643092043493, 0.8, false], "wfo_positive_windows": [0.4, 0.5, false], "research_trades": [138.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-planted-seed2] research: squeeze
*2026-10-01 10:56Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.9333333333333333, "oos_sharpe": 3.157155142907161, "oos_sortino": 7.192632509778909, "oos_mdd": 0.098725838574232, "oos_net_return": 4.0046816912836185, "oos_trades": 501, "oos_profit_factor": 2.137418569878288, "distinct_param_sets_chosen": 3, "median_train_sharpe": 3.8883619512574623}

gates: {"wfo_sharpe": [3.157155142907161, 0.8, true], "wfo_positive_windows": [0.9333333333333333, 0.5, true], "research_trades": [397.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed2] research: ml_gbm
*2026-10-01 10:56Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.06, 'horizon': 6, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 1.0, "oos_sharpe": 5.898664561522433, "oos_sortino": 12.664927488609969, "oos_mdd": 0.10471622403311831, "oos_net_return": 212.96373539138406, "oos_trades": 710, "oos_profit_factor": 3.2230478643078393, "distinct_param_sets_chosen": 4, "median_train_sharpe": 5.825756765711901}

gates: {"wfo_sharpe": [5.898664561522433, 0.8, true], "wfo_positive_windows": [1.0, 0.5, true], "research_trades": [1196.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed2] HOLD-OUT: donchian
*2026-10-01 10:56Z*

params `{'allow_short': True, 'k_atr': 4.0, 'n': 48}`: net=7.834 sharpe=4.80 sortino=10.28 mdd=0.118 pf=3.03 trades=225; DSR=1.000 (strict 0.000); **accepted=True**


### [synthetic-planted-seed2] HOLD-OUT: squeeze
*2026-10-01 10:56Z*

params `{'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2}`: net=1.044 sharpe=2.75 sortino=5.65 mdd=0.095 pf=2.14 trades=196; DSR=1.000 (strict 0.000); **accepted=False**


### [synthetic-planted-seed2] HOLD-OUT: ml_gbm
*2026-10-01 10:58Z*

params `{'delta': 0.06, 'horizon': 6, 'k_atr': 3.0}`: net=7.877 sharpe=4.50 sortino=8.93 mdd=0.156 pf=1.82 trades=625; DSR=1.000 (strict 0.000); **accepted=True**
