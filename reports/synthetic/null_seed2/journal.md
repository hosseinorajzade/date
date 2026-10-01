

### [synthetic-null-seed2] research: donchian
*2026-10-01 10:51Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': False, 'k_atr': 4.0, 'n': 192}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4, "oos_sharpe": -0.24766399643041564, "oos_sortino": -0.40777811273818115, "oos_mdd": 0.3554646651173866, "oos_net_return": -0.15747586144957915, "oos_trades": 182, "oos_profit_factor": 0.8707612843841008, "distinct_param_sets_chosen": 8, "median_train_sharpe": 0.8883778693174689}

gates: {"wfo_sharpe": [-0.24766399643041564, 0.8, false], "wfo_positive_windows": [0.4, 0.5, false], "research_trades": [94.0, 100, false], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed2] research: meanrev
*2026-10-01 10:51Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 3.0, 'lookback': 48, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4666666666666667, "oos_sharpe": -0.03913363238742656, "oos_sortino": -0.0571297573718819, "oos_mdd": 0.20747547368768726, "oos_net_return": -0.024953119358382625, "oos_trades": 185, "oos_profit_factor": 0.9970752539212914, "distinct_param_sets_chosen": 9, "median_train_sharpe": 1.0819421145510164}

gates: {"wfo_sharpe": [-0.03913363238742656, 0.8, false], "wfo_positive_windows": [0.4666666666666667, 0.5, false], "research_trades": [259.0, 100, true], "sensitivity_neighbours_positive": [0.8, 0.6, true]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed2] research: squeeze
*2026-10-01 10:51Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 4.0, 'lookback': 24, 'quantile': 0.1}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.2, "oos_sharpe": -1.2750322828070013, "oos_sortino": -1.9448478841932377, "oos_mdd": 0.5288989642617259, "oos_net_return": -0.4487647682820012, "oos_trades": 474, "oos_profit_factor": 0.7271978618845083, "distinct_param_sets_chosen": 6, "median_train_sharpe": -0.43249786093581866}

gates: {"wfo_sharpe": [-1.2750322828070013, 0.8, false], "wfo_positive_windows": [0.2, 0.5, false], "research_trades": [553.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed2] research: ml_gbm
*2026-10-01 10:51Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.03, 'horizon': 24, 'k_atr': 2.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4666666666666667, "oos_sharpe": 0.23176714288675868, "oos_sortino": 0.4284707318705804, "oos_mdd": 0.5194749990822971, "oos_net_return": 0.1074032433408647, "oos_trades": 819, "oos_profit_factor": 1.048616146742317, "distinct_param_sets_chosen": 4, "median_train_sharpe": 0.5016528940765007}

gates: {"wfo_sharpe": [0.23176714288675868, 0.8, false], "wfo_positive_windows": [0.4666666666666667, 0.5, false], "research_trades": [769.0, 100, true], "sensitivity_neighbours_positive": [0.3333333333333333, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**
