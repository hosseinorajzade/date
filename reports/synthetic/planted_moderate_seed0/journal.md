

### [synthetic-planted-seed0] research: donchian
*2026-10-01 10:55Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': True, 'k_atr': 4.0, 'n': 48}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.8, "oos_sharpe": 4.570170020948587, "oos_sortino": 9.431404903275913, "oos_mdd": 0.16728868370470107, "oos_net_return": 30.738117690276884, "oos_trades": 368, "oos_profit_factor": 3.1235997160838185, "distinct_param_sets_chosen": 7, "median_train_sharpe": 4.873759744532169}

gates: {"wfo_sharpe": [4.570170020948587, 0.8, true], "wfo_positive_windows": [0.8, 0.5, true], "research_trades": [446.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed0] research: meanrev
*2026-10-01 10:56Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": -1.029320855156454, "oos_sortino": -1.3994581163741364, "oos_mdd": 0.2561241861778185, "oos_net_return": -0.22581008803881353, "oos_trades": 120, "oos_profit_factor": 0.6708505376191638, "distinct_param_sets_chosen": 6, "median_train_sharpe": -0.35271624160718623}

gates: {"wfo_sharpe": [-1.029320855156454, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [141.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-planted-seed0] research: squeeze
*2026-10-01 10:56Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.8, "oos_sharpe": 2.9559265670703807, "oos_sortino": 6.277884017263423, "oos_mdd": 0.108456045938647, "oos_net_return": 3.360344901414325, "oos_trades": 584, "oos_profit_factor": 1.895829898772205, "distinct_param_sets_chosen": 3, "median_train_sharpe": 3.1413918587018284}

gates: {"wfo_sharpe": [2.9559265670703807, 0.8, true], "wfo_positive_windows": [0.8, 0.5, true], "research_trades": [816.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed0] research: ml_gbm
*2026-10-01 10:56Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.06, 'horizon': 24, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 1.0, "oos_sharpe": 5.446234335173612, "oos_sortino": 11.832705914375781, "oos_mdd": 0.16238274972158007, "oos_net_return": 183.94128518258748, "oos_trades": 569, "oos_profit_factor": 3.250880561773121, "distinct_param_sets_chosen": 5, "median_train_sharpe": 4.740232778637273}

gates: {"wfo_sharpe": [5.446234335173612, 0.8, true], "wfo_positive_windows": [1.0, 0.5, true], "research_trades": [558.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed0] HOLD-OUT: donchian
*2026-10-01 10:56Z*

params `{'allow_short': True, 'k_atr': 4.0, 'n': 48}`: net=7.275 sharpe=5.04 sortino=10.10 mdd=0.125 pf=3.22 trades=224; DSR=1.000 (strict 0.002); **accepted=True**


### [synthetic-planted-seed0] HOLD-OUT: squeeze
*2026-10-01 10:56Z*

params `{'k_atr': 4.0, 'lookback': 24, 'quantile': 0.2}`: net=1.249 sharpe=2.88 sortino=6.09 mdd=0.109 pf=1.82 trades=360; DSR=1.000 (strict 0.000); **accepted=True**


### [synthetic-planted-seed0] HOLD-OUT: ml_gbm
*2026-10-01 10:58Z*

params `{'delta': 0.06, 'horizon': 24, 'k_atr': 3.0}`: net=10.772 sharpe=4.69 sortino=9.45 mdd=0.109 pf=2.69 trades=317; DSR=1.000 (strict 0.000); **accepted=True**
