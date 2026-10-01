

### [synthetic-null-seed6] research: donchian
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': False, 'k_atr': 2.0, 'n': 24}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": -0.44816407912205114, "oos_sortino": -0.7410347456733469, "oos_mdd": 0.3867648965464082, "oos_net_return": -0.2761031168617142, "oos_trades": 394, "oos_profit_factor": 0.8851999434376199, "distinct_param_sets_chosen": 6, "median_train_sharpe": 0.3029833990314284}

gates: {"wfo_sharpe": [-0.44816407912205114, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [529.0, 100, true], "sensitivity_neighbours_positive": [0.3333333333333333, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed6] research: meanrev
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 3.0, 'lookback': 96, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": -0.7491743121209639, "oos_sortino": -1.0715671798067157, "oos_mdd": 0.3144407126361889, "oos_net_return": -0.2756759612715568, "oos_trades": 397, "oos_profit_factor": 0.8490411035833948, "distinct_param_sets_chosen": 9, "median_train_sharpe": 0.21306214729084014}

gates: {"wfo_sharpe": [-0.7491743121209639, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [177.0, 100, true], "sensitivity_neighbours_positive": [0.5, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed6] research: squeeze
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 2.0, 'lookback': 48, 'quantile': 0.1}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4666666666666667, "oos_sharpe": -0.712134136231734, "oos_sortino": -1.0893814284139134, "oos_mdd": 0.30586503497021567, "oos_net_return": -0.2606146272128911, "oos_trades": 313, "oos_profit_factor": 0.8144537790060152, "distinct_param_sets_chosen": 5, "median_train_sharpe": 0.3118853728207069}

gates: {"wfo_sharpe": [-0.712134136231734, 0.8, false], "wfo_positive_windows": [0.4666666666666667, 0.5, false], "research_trades": [334.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed6] research: ml_gbm
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.06, 'horizon': 24, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.13333333333333333, "oos_sharpe": -1.5813863409853823, "oos_sortino": -2.3170258150275567, "oos_mdd": 0.7426308251992134, "oos_net_return": -0.6817122355636257, "oos_trades": 997, "oos_profit_factor": 0.7688761777103125, "distinct_param_sets_chosen": 6, "median_train_sharpe": 0.12800388091011727}

gates: {"wfo_sharpe": [-1.5813863409853823, 0.8, false], "wfo_positive_windows": [0.13333333333333333, 0.5, false], "research_trades": [779.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**
