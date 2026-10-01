

### [synthetic-null-seed3] research: donchian
*2026-10-01 10:51Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': False, 'k_atr': 4.0, 'n': 96}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": -0.3121993524301442, "oos_sortino": -0.5238608957937351, "oos_mdd": 0.38150855548919205, "oos_net_return": -0.1785825105647204, "oos_trades": 217, "oos_profit_factor": 0.8719443659660402, "distinct_param_sets_chosen": 9, "median_train_sharpe": 0.7788125192376335}

gates: {"wfo_sharpe": [-0.3121993524301442, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [163.0, 100, true], "sensitivity_neighbours_positive": [0.75, 0.6, true]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed3] research: meanrev
*2026-10-01 10:51Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 3.0, 'lookback': 96, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": -0.14017006056580644, "oos_sortino": -0.22285023263766307, "oos_mdd": 0.30335722765760187, "oos_net_return": -0.06924978887647282, "oos_trades": 220, "oos_profit_factor": 0.9652415680547829, "distinct_param_sets_chosen": 8, "median_train_sharpe": 1.1652920211508762}

gates: {"wfo_sharpe": [-0.14017006056580644, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [181.0, 100, true], "sensitivity_neighbours_positive": [0.75, 0.6, true]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed3] research: squeeze
*2026-10-01 10:51Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 3.0, 'lookback': 48, 'quantile': 0.2}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.2, "oos_sharpe": -0.5852188860094324, "oos_sortino": -0.9252789210287988, "oos_mdd": 0.36213319569806224, "oos_net_return": -0.2201387705177511, "oos_trades": 310, "oos_profit_factor": 0.8483895235168541, "distinct_param_sets_chosen": 6, "median_train_sharpe": -0.8350808617803017}

gates: {"wfo_sharpe": [-0.5852188860094324, 0.8, false], "wfo_positive_windows": [0.2, 0.5, false], "research_trades": [458.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed3] research: ml_gbm
*2026-10-01 10:51Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.06, 'horizon': 24, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.2, "oos_sharpe": -1.120709157353726, "oos_sortino": -1.8173535145428068, "oos_mdd": 0.6022625895370761, "oos_net_return": -0.5782882078985592, "oos_trades": 1097, "oos_profit_factor": 0.8288718498799555, "distinct_param_sets_chosen": 6, "median_train_sharpe": -0.8095746505202519}

gates: {"wfo_sharpe": [-1.120709157353726, 0.8, false], "wfo_positive_windows": [0.2, 0.5, false], "research_trades": [737.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**
