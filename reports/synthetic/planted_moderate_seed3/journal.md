

### [synthetic-planted-seed3] research: donchian
*2026-10-01 10:56Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': True, 'k_atr': 4.0, 'n': 96}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.9333333333333333, "oos_sharpe": 3.0554491372447194, "oos_sortino": 6.428630978876625, "oos_mdd": 0.11956601123373167, "oos_net_return": 9.698704229969854, "oos_trades": 252, "oos_profit_factor": 3.036831186282094, "distinct_param_sets_chosen": 7, "median_train_sharpe": 5.7024003708116116}

gates: {"wfo_sharpe": [3.0554491372447194, 0.8, true], "wfo_positive_windows": [0.9333333333333333, 0.5, true], "research_trades": [252.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed3] research: meanrev
*2026-10-01 10:56Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 2.0, 'lookback': 96, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4, "oos_sharpe": -1.0518343240791719, "oos_sortino": -1.4679202084150942, "oos_mdd": 0.35676365896424456, "oos_net_return": -0.27171234701158276, "oos_trades": 139, "oos_profit_factor": 0.6885503086921102, "distinct_param_sets_chosen": 6, "median_train_sharpe": -0.01348618050912053}

gates: {"wfo_sharpe": [-1.0518343240791719, 0.8, false], "wfo_positive_windows": [0.4, 0.5, false], "research_trades": [145.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-planted-seed3] research: squeeze
*2026-10-01 10:56Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.8666666666666667, "oos_sharpe": 2.725682078388882, "oos_sortino": 5.829044374033124, "oos_mdd": 0.1198639916104135, "oos_net_return": 2.6580448491695736, "oos_trades": 394, "oos_profit_factor": 1.9762260849904476, "distinct_param_sets_chosen": 3, "median_train_sharpe": 3.6341088815131575}

gates: {"wfo_sharpe": [2.725682078388882, 0.8, true], "wfo_positive_windows": [0.8666666666666667, 0.5, true], "research_trades": [386.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed3] research: ml_gbm
*2026-10-01 10:56Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.06, 'horizon': 6, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.8666666666666667, "oos_sharpe": 3.5614190195552866, "oos_sortino": 7.0902458725914, "oos_mdd": 0.1966637457576872, "oos_net_return": 33.10539371271625, "oos_trades": 741, "oos_profit_factor": 2.170061298538872, "distinct_param_sets_chosen": 5, "median_train_sharpe": 4.893911803653699}

gates: {"wfo_sharpe": [3.5614190195552866, 0.8, true], "wfo_positive_windows": [0.8666666666666667, 0.5, true], "research_trades": [1239.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed3] HOLD-OUT: donchian
*2026-10-01 10:56Z*

params `{'allow_short': True, 'k_atr': 4.0, 'n': 96}`: net=3.403 sharpe=4.52 sortino=8.95 mdd=0.072 pf=3.09 trades=110; DSR=1.000 (strict 0.001); **accepted=False**


### [synthetic-planted-seed3] HOLD-OUT: squeeze
*2026-10-01 10:56Z*

params `{'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2}`: net=0.958 sharpe=2.38 sortino=4.84 mdd=0.115 pf=1.97 trades=208; DSR=0.998 (strict 0.000); **accepted=True**


### [synthetic-planted-seed3] HOLD-OUT: ml_gbm
*2026-10-01 10:58Z*

params `{'delta': 0.06, 'horizon': 6, 'k_atr': 3.0}`: net=6.572 sharpe=4.47 sortino=9.15 mdd=0.111 pf=1.87 trades=684; DSR=1.000 (strict 0.001); **accepted=True**
