

### [synthetic-null-seed4] research: donchian
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': False, 'k_atr': 2.0, 'n': 192}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4, "oos_sharpe": -0.5116820365301108, "oos_sortino": -0.7901653028970473, "oos_mdd": 0.307393702619675, "oos_net_return": -0.254663184018426, "oos_trades": 208, "oos_profit_factor": 0.7984688238082058, "distinct_param_sets_chosen": 7, "median_train_sharpe": 1.1751000220886447}

gates: {"wfo_sharpe": [-0.5116820365301108, 0.8, false], "wfo_positive_windows": [0.4, 0.5, false], "research_trades": [101.0, 100, true], "sensitivity_neighbours_positive": [0.6666666666666666, 0.6, true]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed4] research: meanrev
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 1.01, 'k_atr': 3.0, 'lookback': 96, 'z_in': 2.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.5333333333333333, "oos_sharpe": 0.294119666744203, "oos_sortino": 0.4840924239271332, "oos_mdd": 0.26163636775974497, "oos_net_return": 0.1063159319014313, "oos_trades": 261, "oos_profit_factor": 1.0840090376157356, "distinct_param_sets_chosen": 7, "median_train_sharpe": 0.737890294213273}

gates: {"wfo_sharpe": [0.294119666744203, 0.8, false], "wfo_positive_windows": [0.5333333333333333, 0.5, true], "research_trades": [439.0, 100, true], "sensitivity_neighbours_positive": [0.75, 0.6, true]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed4] research: squeeze
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4666666666666667, "oos_sharpe": 0.18663033544359478, "oos_sortino": 0.3037811365773313, "oos_mdd": 0.2339991623792922, "oos_net_return": 0.05785445075932305, "oos_trades": 425, "oos_profit_factor": 1.0509687029332329, "distinct_param_sets_chosen": 5, "median_train_sharpe": 0.2871372071178008}

gates: {"wfo_sharpe": [0.18663033544359478, 0.8, false], "wfo_positive_windows": [0.4666666666666667, 0.5, false], "research_trades": [432.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed4] research: ml_gbm
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.06, 'horizon': 24, 'k_atr': 2.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": -0.7528407078441891, "oos_sortino": -1.1960008070686745, "oos_mdd": 0.540042283641538, "oos_net_return": -0.45339028740362153, "oos_trades": 656, "oos_profit_factor": 0.8548634080171177, "distinct_param_sets_chosen": 4, "median_train_sharpe": 0.27828998029065655}

gates: {"wfo_sharpe": [-0.7528407078441891, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [729.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**
