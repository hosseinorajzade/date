

### [synthetic-null-seed7] research: donchian
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': True, 'k_atr': 3.0, 'n': 48}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": -0.2604708372645143, "oos_sortino": -0.44477467656505143, "oos_mdd": 0.334442946032385, "oos_net_return": -0.16940847385981406, "oos_trades": 190, "oos_profit_factor": 0.8937910236904973, "distinct_param_sets_chosen": 8, "median_train_sharpe": -0.12343812060914523}

gates: {"wfo_sharpe": [-0.2604708372645143, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [564.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed7] research: meanrev
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 2.0, 'lookback': 96, 'z_in': 2.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4666666666666667, "oos_sharpe": -0.6875464243153809, "oos_sortino": -0.9678722280197023, "oos_mdd": 0.31722583442784735, "oos_net_return": -0.21894324416554323, "oos_trades": 268, "oos_profit_factor": 0.8449952710588728, "distinct_param_sets_chosen": 6, "median_train_sharpe": 1.0838180862321172}

gates: {"wfo_sharpe": [-0.6875464243153809, 0.8, false], "wfo_positive_windows": [0.4666666666666667, 0.5, false], "research_trades": [449.0, 100, true], "sensitivity_neighbours_positive": [0.25, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed7] research: squeeze
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 4.0, 'lookback': 24, 'quantile': 0.1}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4, "oos_sharpe": -0.7582460477898593, "oos_sortino": -1.2030986201940665, "oos_mdd": 0.3161536240943075, "oos_net_return": -0.26603354913952015, "oos_trades": 373, "oos_profit_factor": 0.792778182443737, "distinct_param_sets_chosen": 7, "median_train_sharpe": 0.12631442753862138}

gates: {"wfo_sharpe": [-0.7582460477898593, 0.8, false], "wfo_positive_windows": [0.4, 0.5, false], "research_trades": [554.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed7] research: ml_gbm
*2026-10-01 10:52Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.06, 'horizon': 24, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.13333333333333333, "oos_sharpe": -1.412350042296219, "oos_sortino": -2.1024563559134717, "oos_mdd": 0.6517042714918192, "oos_net_return": -0.6154825139049463, "oos_trades": 678, "oos_profit_factor": 0.7668580268727474, "distinct_param_sets_chosen": 4, "median_train_sharpe": -0.42707236851883423}

gates: {"wfo_sharpe": [-1.412350042296219, 0.8, false], "wfo_positive_windows": [0.13333333333333333, 0.5, false], "research_trades": [712.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**
