

### [synthetic-planted-seed3] research: donchian
*2026-10-01 10:53Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': True, 'k_atr': 2.0, 'n': 96}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4666666666666667, "oos_sharpe": 0.3622532468409341, "oos_sortino": 0.56744103506366, "oos_mdd": 0.23988211967719586, "oos_net_return": 0.1667993201773268, "oos_trades": 192, "oos_profit_factor": 1.159346950141998, "distinct_param_sets_chosen": 9, "median_train_sharpe": 2.5552168600925986}

gates: {"wfo_sharpe": [0.3622532468409341, 0.8, false], "wfo_positive_windows": [0.4666666666666667, 0.5, false], "research_trades": [304.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-planted-seed3] research: meanrev
*2026-10-01 10:53Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 3.0, 'lookback': 48, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4, "oos_sharpe": -0.7199504201597489, "oos_sortino": -1.0509951359651513, "oos_mdd": 0.39989531755808827, "oos_net_return": -0.23517588402051748, "oos_trades": 296, "oos_profit_factor": 0.831504361937753, "distinct_param_sets_chosen": 10, "median_train_sharpe": 0.2902967379679777}

gates: {"wfo_sharpe": [-0.7199504201597489, 0.8, false], "wfo_positive_windows": [0.4, 0.5, false], "research_trades": [255.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-planted-seed3] research: squeeze
*2026-10-01 10:53Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4666666666666667, "oos_sharpe": 0.11877166298074532, "oos_sortino": 0.2108708301583855, "oos_mdd": 0.28750439776584547, "oos_net_return": 0.026469097204121272, "oos_trades": 429, "oos_profit_factor": 1.0565275587937022, "distinct_param_sets_chosen": 8, "median_train_sharpe": 0.35819665771768155}

gates: {"wfo_sharpe": [0.11877166298074532, 0.8, false], "wfo_positive_windows": [0.4666666666666667, 0.5, false], "research_trades": [447.0, 100, true], "sensitivity_neighbours_positive": [0.6666666666666666, 0.6, true]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-planted-seed3] research: ml_gbm
*2026-10-01 10:54Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.06, 'horizon': 24, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.6666666666666666, "oos_sharpe": 1.0038091067730375, "oos_sortino": 1.6185466501295749, "oos_mdd": 0.2974356577269508, "oos_net_return": 0.9784055669253082, "oos_trades": 574, "oos_profit_factor": 1.2263843490957516, "distinct_param_sets_chosen": 3, "median_train_sharpe": 1.6062704519851119}

gates: {"wfo_sharpe": [1.0038091067730375, 0.8, true], "wfo_positive_windows": [0.6666666666666666, 0.5, true], "research_trades": [649.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed3] HOLD-OUT: ml_gbm
*2026-10-01 10:55Z*

params `{'delta': 0.06, 'horizon': 24, 'k_atr': 3.0}`: net=0.237 sharpe=0.60 sortino=1.02 mdd=0.225 pf=1.11 trades=370; DSR=0.443 (strict 0.001); **accepted=False**
