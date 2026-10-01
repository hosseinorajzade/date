

### [synthetic-null-seed9] research: donchian
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': False, 'k_atr': 3.0, 'n': 192}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4, "oos_sharpe": 0.0029946477215822744, "oos_sortino": 0.004978606658757497, "oos_mdd": 0.30830896971705135, "oos_net_return": -0.03488903198959192, "oos_trades": 170, "oos_profit_factor": 0.9950491195792467, "distinct_param_sets_chosen": 10, "median_train_sharpe": 0.2801795597443483}

gates: {"wfo_sharpe": [0.0029946477215822744, 0.8, false], "wfo_positive_windows": [0.4, 0.5, false], "research_trades": [95.0, 100, false], "sensitivity_neighbours_positive": [0.5, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed9] research: meanrev
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 1.01, 'k_atr': 3.0, 'lookback': 96, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": -0.8283592709796633, "oos_sortino": -1.175210737330033, "oos_mdd": 0.32036236821926445, "oos_net_return": -0.2512783751039017, "oos_trades": 207, "oos_profit_factor": 0.7842048450045187, "distinct_param_sets_chosen": 8, "median_train_sharpe": 0.7466758342161758}

gates: {"wfo_sharpe": [-0.8283592709796633, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [180.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed9] research: squeeze
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 2.0, 'lookback': 48, 'quantile': 0.2}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.26666666666666666, "oos_sharpe": -0.2704493075599986, "oos_sortino": -0.4457741318900362, "oos_mdd": 0.27467803338982655, "oos_net_return": -0.13921955555089283, "oos_trades": 424, "oos_profit_factor": 0.9354577442305047, "distinct_param_sets_chosen": 7, "median_train_sharpe": 0.19462327413757238}

gates: {"wfo_sharpe": [-0.2704493075599986, 0.8, false], "wfo_positive_windows": [0.26666666666666666, 0.5, false], "research_trades": [440.0, 100, true], "sensitivity_neighbours_positive": [0.3333333333333333, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed9] research: ml_gbm
*2026-10-01 10:53Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.03, 'horizon': 24, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": 0.20198356443012222, "oos_sortino": 0.3437855742093183, "oos_mdd": 0.38215042404000465, "oos_net_return": 0.07894382779553766, "oos_trades": 722, "oos_profit_factor": 1.0473073490662759, "distinct_param_sets_chosen": 4, "median_train_sharpe": 0.5746827124301478}

gates: {"wfo_sharpe": [0.20198356443012222, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [745.0, 100, true], "sensitivity_neighbours_positive": [0.3333333333333333, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**
