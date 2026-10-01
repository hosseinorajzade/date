

### [synthetic-planted-seed1] research: donchian
*2026-10-01 10:53Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': True, 'k_atr': 3.0, 'n': 192}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.8, "oos_sharpe": 1.9325948385308058, "oos_sortino": 3.6346235240740796, "oos_mdd": 0.16075388096798393, "oos_net_return": 2.4322049886974977, "oos_trades": 177, "oos_profit_factor": 2.123718504097746, "distinct_param_sets_chosen": 8, "median_train_sharpe": 2.4676265950401213}

gates: {"wfo_sharpe": [1.9325948385308058, 0.8, true], "wfo_positive_windows": [0.8, 0.5, true], "research_trades": [159.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed1] research: meanrev
*2026-10-01 10:53Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 3.0, 'lookback': 48, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.26666666666666666, "oos_sharpe": -0.9417735659715226, "oos_sortino": -1.346680867798015, "oos_mdd": 0.3985964489827213, "oos_net_return": -0.3107709314362638, "oos_trades": 348, "oos_profit_factor": 0.7980778726170451, "distinct_param_sets_chosen": 7, "median_train_sharpe": 0.17554501501575084}

gates: {"wfo_sharpe": [-0.9417735659715226, 0.8, false], "wfo_positive_windows": [0.26666666666666666, 0.5, false], "research_trades": [249.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-planted-seed1] research: squeeze
*2026-10-01 10:53Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.6666666666666666, "oos_sharpe": 1.2340228136510054, "oos_sortino": 2.3000247813265022, "oos_mdd": 0.1640152312998251, "oos_net_return": 0.6777497097482506, "oos_trades": 462, "oos_profit_factor": 1.3577746029066762, "distinct_param_sets_chosen": 5, "median_train_sharpe": 1.458397117361731}

gates: {"wfo_sharpe": [1.2340228136510054, 0.8, true], "wfo_positive_windows": [0.6666666666666666, 0.5, true], "research_trades": [461.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed1] research: ml_gbm
*2026-10-01 10:54Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.06, 'horizon': 24, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.7333333333333333, "oos_sharpe": 1.4990995500284234, "oos_sortino": 2.6474457265198175, "oos_mdd": 0.17872420786168763, "oos_net_return": 2.3319239235159044, "oos_trades": 647, "oos_profit_factor": 1.349576729116856, "distinct_param_sets_chosen": 5, "median_train_sharpe": 2.2426718335390246}

gates: {"wfo_sharpe": [1.4990995500284234, 0.8, true], "wfo_positive_windows": [0.7333333333333333, 0.5, true], "research_trades": [665.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed1] HOLD-OUT: donchian
*2026-10-01 10:54Z*

params `{'allow_short': True, 'k_atr': 3.0, 'n': 192}`: net=0.640 sharpe=1.47 sortino=2.41 mdd=0.165 pf=1.71 trades=80; DSR=0.881 (strict 0.010); **accepted=False**


### [synthetic-planted-seed1] HOLD-OUT: squeeze
*2026-10-01 10:54Z*

params `{'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2}`: net=0.027 sharpe=0.16 sortino=0.26 mdd=0.212 pf=1.03 trades=230; DSR=0.210 (strict 0.000); **accepted=False**


### [synthetic-planted-seed1] HOLD-OUT: ml_gbm
*2026-10-01 10:55Z*

params `{'delta': 0.06, 'horizon': 24, 'k_atr': 3.0}`: net=0.524 sharpe=1.08 sortino=1.80 mdd=0.208 pf=1.22 trades=358; DSR=0.722 (strict 0.002); **accepted=False**
