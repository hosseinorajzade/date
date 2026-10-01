

### [synthetic-planted-seed2] research: donchian
*2026-10-01 10:53Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': True, 'k_atr': 4.0, 'n': 192}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.7333333333333333, "oos_sharpe": 1.850119554387087, "oos_sortino": 3.3699171419075626, "oos_mdd": 0.19220128943670534, "oos_net_return": 1.8795827046673481, "oos_trades": 243, "oos_profit_factor": 1.8882983752199394, "distinct_param_sets_chosen": 8, "median_train_sharpe": 3.1105729221464267}

gates: {"wfo_sharpe": [1.850119554387087, 0.8, true], "wfo_positive_windows": [0.7333333333333333, 0.5, true], "research_trades": [155.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed2] research: meanrev
*2026-10-01 10:53Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 2.0, 'lookback': 24, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4666666666666667, "oos_sharpe": -0.2507874497111645, "oos_sortino": -0.3664757442705627, "oos_mdd": 0.1399335463938678, "oos_net_return": -0.08164417779342148, "oos_trades": 179, "oos_profit_factor": 0.9239852370017753, "distinct_param_sets_chosen": 7, "median_train_sharpe": 0.5175966343154008}

gates: {"wfo_sharpe": [-0.2507874497111645, 0.8, false], "wfo_positive_windows": [0.4666666666666667, 0.5, false], "research_trades": [157.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-planted-seed2] research: squeeze
*2026-10-01 10:53Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": 0.22161655871695934, "oos_sortino": 0.39207191080806497, "oos_mdd": 0.2786106718469539, "oos_net_return": 0.0736548666186363, "oos_trades": 482, "oos_profit_factor": 1.060169204823351, "distinct_param_sets_chosen": 6, "median_train_sharpe": 1.0145980146312439}

gates: {"wfo_sharpe": [0.22161655871695934, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [445.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-planted-seed2] research: ml_gbm
*2026-10-01 10:54Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.03, 'horizon': 24, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.8666666666666667, "oos_sharpe": 2.4781830085861607, "oos_sortino": 4.689375583196391, "oos_mdd": 0.14340389207475146, "oos_net_return": 7.787743052336971, "oos_trades": 624, "oos_profit_factor": 1.6798336951219728, "distinct_param_sets_chosen": 3, "median_train_sharpe": 3.1524981665796727}

gates: {"wfo_sharpe": [2.4781830085861607, 0.8, true], "wfo_positive_windows": [0.8666666666666667, 0.5, true], "research_trades": [617.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed2] HOLD-OUT: donchian
*2026-10-01 10:54Z*

params `{'allow_short': True, 'k_atr': 4.0, 'n': 192}`: net=0.132 sharpe=0.50 sortino=0.76 mdd=0.117 pf=1.24 trades=72; DSR=0.399 (strict 0.000); **accepted=False**


### [synthetic-planted-seed2] HOLD-OUT: ml_gbm
*2026-10-01 10:55Z*

params `{'delta': 0.03, 'horizon': 24, 'k_atr': 3.0}`: net=-0.222 sharpe=-0.53 sortino=-0.75 mdd=0.312 pf=0.88 trades=305; DSR=0.037 (strict 0.000); **accepted=False**
