

### [synthetic-null-seed5] research: donchian
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': True, 'k_atr': 2.0, 'n': 192}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": 0.20576397095784552, "oos_sortino": 0.35710985366459486, "oos_mdd": 0.1791260839462948, "oos_net_return": 0.07320880182630374, "oos_trades": 116, "oos_profit_factor": 1.1464889452731089, "distinct_param_sets_chosen": 6, "median_train_sharpe": 1.0168551279218785}

gates: {"wfo_sharpe": [0.20576397095784552, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [176.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed5] research: meanrev
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 3.0, 'lookback': 96, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": -1.0709887829865454, "oos_sortino": -1.4532604529376192, "oos_mdd": 0.3379719167749652, "oos_net_return": -0.31580372407691193, "oos_trades": 280, "oos_profit_factor": 0.765832406412778, "distinct_param_sets_chosen": 10, "median_train_sharpe": 0.1309169883493174}

gates: {"wfo_sharpe": [-1.0709887829865454, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [180.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed5] research: squeeze
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 3.0, 'lookback': 48, 'quantile': 0.2}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4, "oos_sharpe": -0.261495074612455, "oos_sortino": -0.42206618190922246, "oos_mdd": 0.22850813669248127, "oos_net_return": -0.11787513584813558, "oos_trades": 375, "oos_profit_factor": 0.9280345213737253, "distinct_param_sets_chosen": 6, "median_train_sharpe": -0.01584104579924137}

gates: {"wfo_sharpe": [-0.261495074612455, 0.8, false], "wfo_positive_windows": [0.4, 0.5, false], "research_trades": [456.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed5] research: ml_gbm
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.06, 'horizon': 6, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.13333333333333333, "oos_sharpe": -2.1368139477473624, "oos_sortino": -3.0007753919422986, "oos_mdd": 0.7764845205805022, "oos_net_return": -0.7660992749721057, "oos_trades": 1037, "oos_profit_factor": 0.7167627385165329, "distinct_param_sets_chosen": 6, "median_train_sharpe": -0.44158473943988397}

gates: {"wfo_sharpe": [-2.1368139477473624, 0.8, false], "wfo_positive_windows": [0.13333333333333333, 0.5, false], "research_trades": [1282.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**
