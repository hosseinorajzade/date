

### [synthetic-null-seed10] research: donchian
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': False, 'k_atr': 4.0, 'n': 96}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.2, "oos_sharpe": -0.4328613996390767, "oos_sortino": -0.6803211121556739, "oos_mdd": 0.27042374260901303, "oos_net_return": -0.24251228641340983, "oos_trades": 248, "oos_profit_factor": 0.8398759519782423, "distinct_param_sets_chosen": 9, "median_train_sharpe": 0.04468825100090262}

gates: {"wfo_sharpe": [-0.4328613996390767, 0.8, false], "wfo_positive_windows": [0.2, 0.5, false], "research_trades": [168.0, 100, true], "sensitivity_neighbours_positive": [0.25, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed10] research: meanrev
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 3.0, 'lookback': 48, 'z_in': 2.5}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": -1.1568788045396667, "oos_sortino": -1.6007159257642105, "oos_mdd": 0.4713809696051855, "oos_net_return": -0.35990009273835666, "oos_trades": 330, "oos_profit_factor": 0.7746759836766764, "distinct_param_sets_chosen": 9, "median_train_sharpe": -0.31313839994183795}

gates: {"wfo_sharpe": [-1.1568788045396667, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [495.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed10] research: squeeze
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 2.0, 'lookback': 24, 'quantile': 0.1}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.2, "oos_sharpe": -1.3280540898684894, "oos_sortino": -1.955453481213128, "oos_mdd": 0.5194406223393888, "oos_net_return": -0.4575402881302114, "oos_trades": 425, "oos_profit_factor": 0.7019940480501092, "distinct_param_sets_chosen": 9, "median_train_sharpe": -0.1935043610760429}

gates: {"wfo_sharpe": [-1.3280540898684894, 0.8, false], "wfo_positive_windows": [0.2, 0.5, false], "research_trades": [556.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed10] research: ml_gbm
*2026-10-01 10:53Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.06, 'horizon': 24, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": -0.39864407346989944, "oos_sortino": -0.6395790698280659, "oos_mdd": 0.3794060104648548, "oos_net_return": -0.29757357034022325, "oos_trades": 686, "oos_profit_factor": 0.9189210574254858, "distinct_param_sets_chosen": 3, "median_train_sharpe": 0.16653338944546786}

gates: {"wfo_sharpe": [-0.39864407346989944, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [757.0, 100, true], "sensitivity_neighbours_positive": [0.3333333333333333, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**
