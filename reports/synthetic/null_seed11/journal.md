

### [synthetic-null-seed11] research: donchian
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': True, 'k_atr': 2.0, 'n': 192}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4666666666666667, "oos_sharpe": -0.6911860186656106, "oos_sortino": -1.0765899656724955, "oos_mdd": 0.522535898569819, "oos_net_return": -0.39022868992498516, "oos_trades": 410, "oos_profit_factor": 0.8224252482428345, "distinct_param_sets_chosen": 10, "median_train_sharpe": 0.615575932799826}

gates: {"wfo_sharpe": [-0.6911860186656106, 0.8, false], "wfo_positive_windows": [0.4666666666666667, 0.5, false], "research_trades": [180.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed11] research: meanrev
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 3.0, 'lookback': 96, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4, "oos_sharpe": -0.6666484856354009, "oos_sortino": -0.9610271146752207, "oos_mdd": 0.2783589249887577, "oos_net_return": -0.22909125957003373, "oos_trades": 258, "oos_profit_factor": 0.8393482411047617, "distinct_param_sets_chosen": 12, "median_train_sharpe": 0.8324435815536123}

gates: {"wfo_sharpe": [-0.6666484856354009, 0.8, false], "wfo_positive_windows": [0.4, 0.5, false], "research_trades": [186.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed11] research: squeeze
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 3.0, 'lookback': 48, 'quantile': 0.1}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4666666666666667, "oos_sharpe": -0.5064617385311382, "oos_sortino": -0.8304847114690724, "oos_mdd": 0.2857776612850027, "oos_net_return": -0.21117037581209508, "oos_trades": 335, "oos_profit_factor": 0.8585414432722884, "distinct_param_sets_chosen": 7, "median_train_sharpe": -0.06463116541138145}

gates: {"wfo_sharpe": [-0.5064617385311382, 0.8, false], "wfo_positive_windows": [0.4666666666666667, 0.5, false], "research_trades": [327.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed11] research: ml_gbm
*2026-10-01 10:53Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.06, 'horizon': 24, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.26666666666666666, "oos_sharpe": -0.9421445141270064, "oos_sortino": -1.4578970818432362, "oos_mdd": 0.5927343670965992, "oos_net_return": -0.5252095197591843, "oos_trades": 806, "oos_profit_factor": 0.855146679771556, "distinct_param_sets_chosen": 5, "median_train_sharpe": -0.47466312253092136}

gates: {"wfo_sharpe": [-0.9421445141270064, 0.8, false], "wfo_positive_windows": [0.26666666666666666, 0.5, false], "research_trades": [755.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**
