

### [synthetic-null-seed8] research: donchian
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': True, 'k_atr': 3.0, 'n': 192}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4, "oos_sharpe": -0.4697163746617886, "oos_sortino": -0.6844473670039748, "oos_mdd": 0.3665819570660179, "oos_net_return": -0.25093288343994835, "oos_trades": 240, "oos_profit_factor": 0.8172001301679741, "distinct_param_sets_chosen": 9, "median_train_sharpe": 0.9845408363619584}

gates: {"wfo_sharpe": [-0.4697163746617886, 0.8, false], "wfo_positive_windows": [0.4, 0.5, false], "research_trades": [173.0, 100, true], "sensitivity_neighbours_positive": [0.75, 0.6, true]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed8] research: meanrev
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 3.0, 'lookback': 48, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.2, "oos_sharpe": -1.4866231735239015, "oos_sortino": -2.0647349517736, "oos_mdd": 0.43220415995858164, "oos_net_return": -0.40513697528238, "oos_trades": 224, "oos_profit_factor": 0.6593031852953802, "distinct_param_sets_chosen": 9, "median_train_sharpe": 0.20504419140344685}

gates: {"wfo_sharpe": [-1.4866231735239015, 0.8, false], "wfo_positive_windows": [0.2, 0.5, false], "research_trades": [255.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed8] research: squeeze
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 4.0, 'lookback': 24, 'quantile': 0.1}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.06666666666666667, "oos_sharpe": -1.5301667936124137, "oos_sortino": -2.251309864302828, "oos_mdd": 0.4581683298628355, "oos_net_return": -0.43689600943577256, "oos_trades": 424, "oos_profit_factor": 0.654893604489861, "distinct_param_sets_chosen": 7, "median_train_sharpe": -0.5025829208773596}

gates: {"wfo_sharpe": [-1.5301667936124137, 0.8, false], "wfo_positive_windows": [0.06666666666666667, 0.5, false], "research_trades": [574.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed8] research: ml_gbm
*2026-10-01 10:53Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.03, 'horizon': 24, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4, "oos_sharpe": -0.5192977524611151, "oos_sortino": -0.7875386498884304, "oos_mdd": 0.4789216227311992, "oos_net_return": -0.34165634320791205, "oos_trades": 659, "oos_profit_factor": 0.9119335210339762, "distinct_param_sets_chosen": 3, "median_train_sharpe": -0.008564090185930876}

gates: {"wfo_sharpe": [-0.5192977524611151, 0.8, false], "wfo_positive_windows": [0.4, 0.5, false], "research_trades": [735.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**
