

### [synthetic-null-seed1] research: donchian
*2026-10-01 10:51Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': True, 'k_atr': 4.0, 'n': 192}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4666666666666667, "oos_sharpe": -0.022184570953806555, "oos_sortino": -0.03320591352003213, "oos_mdd": 0.25866408530476914, "oos_net_return": -0.04413199496511078, "oos_trades": 298, "oos_profit_factor": 0.9801297122968172, "distinct_param_sets_chosen": 7, "median_train_sharpe": 0.8781723995423674}

gates: {"wfo_sharpe": [-0.022184570953806555, 0.8, false], "wfo_positive_windows": [0.4666666666666667, 0.5, false], "research_trades": [165.0, 100, true], "sensitivity_neighbours_positive": [0.6666666666666666, 0.6, true]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed1] research: meanrev
*2026-10-01 10:51Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.2, "oos_sharpe": -1.3469548641216205, "oos_sortino": -1.828487195484762, "oos_mdd": 0.40991356165125303, "oos_net_return": -0.385292883230838, "oos_trades": 294, "oos_profit_factor": 0.7101338193322211, "distinct_param_sets_chosen": 12, "median_train_sharpe": 0.8755265360194711}

gates: {"wfo_sharpe": [-1.3469548641216205, 0.8, false], "wfo_positive_windows": [0.2, 0.5, false], "research_trades": [177.0, 100, true], "sensitivity_neighbours_positive": [0.25, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed1] research: squeeze
*2026-10-01 10:51Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 4.0, 'lookback': 48, 'quantile': 0.1}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": -0.9277140118813341, "oos_sortino": -1.457911183224029, "oos_mdd": 0.4246898233256552, "oos_net_return": -0.35230493138819496, "oos_trades": 412, "oos_profit_factor": 0.7829594163951006, "distinct_param_sets_chosen": 8, "median_train_sharpe": -0.11728959362562094}

gates: {"wfo_sharpe": [-0.9277140118813341, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [354.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed1] research: ml_gbm
*2026-10-01 10:51Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.06, 'horizon': 24, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.6, "oos_sharpe": 0.36988668303245065, "oos_sortino": 0.6372243343829445, "oos_mdd": 0.2599919039442473, "oos_net_return": 0.22105426411211204, "oos_trades": 710, "oos_profit_factor": 1.059621546466788, "distinct_param_sets_chosen": 4, "median_train_sharpe": 0.35955515887817585}

gates: {"wfo_sharpe": [0.36988668303245065, 0.8, false], "wfo_positive_windows": [0.6, 0.5, true], "research_trades": [795.0, 100, true], "sensitivity_neighbours_positive": [0.3333333333333333, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**
