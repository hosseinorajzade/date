

### [synthetic-null-seed0] research: donchian
*2026-10-01 10:51Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': True, 'k_atr': 3.0, 'n': 96}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": -0.03231230249071236, "oos_sortino": -0.05023831387035005, "oos_mdd": 0.3447163226175127, "oos_net_return": -0.07263210577272117, "oos_trades": 380, "oos_profit_factor": 0.9994705366388306, "distinct_param_sets_chosen": 8, "median_train_sharpe": 0.7641109372996011}

gates: {"wfo_sharpe": [-0.03231230249071236, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [306.0, 100, true], "sensitivity_neighbours_positive": [0.6, 0.6, true]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed0] research: meanrev
*2026-10-01 10:51Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 2.0, 'lookback': 48, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.26666666666666666, "oos_sharpe": -0.793379415431036, "oos_sortino": -1.1574088661651862, "oos_mdd": 0.319467854156007, "oos_net_return": -0.2721266143245672, "oos_trades": 284, "oos_profit_factor": 0.8205320777340676, "distinct_param_sets_chosen": 10, "median_train_sharpe": 0.19042476117905496}

gates: {"wfo_sharpe": [-0.793379415431036, 0.8, false], "wfo_positive_windows": [0.26666666666666666, 0.5, false], "research_trades": [221.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed0] research: squeeze
*2026-10-01 10:51Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 4.0, 'lookback': 48, 'quantile': 0.1}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": -0.5703159313084718, "oos_sortino": -0.9331173691506418, "oos_mdd": 0.31966258267851233, "oos_net_return": -0.2135272455017383, "oos_trades": 365, "oos_profit_factor": 0.8501606368854094, "distinct_param_sets_chosen": 6, "median_train_sharpe": 0.2986645317051132}

gates: {"wfo_sharpe": [-0.5703159313084718, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [324.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-null-seed0] research: ml_gbm
*2026-10-01 10:51Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.06, 'horizon': 24, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": -0.5068940662255084, "oos_sortino": -0.7976179721131695, "oos_mdd": 0.4507473782015714, "oos_net_return": -0.36744799471597367, "oos_trades": 706, "oos_profit_factor": 0.9095968425822611, "distinct_param_sets_chosen": 3, "median_train_sharpe": -0.6055207057756761}

gates: {"wfo_sharpe": [-0.5068940662255084, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [720.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**
