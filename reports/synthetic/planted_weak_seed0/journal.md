

### [synthetic-planted-seed0] research: donchian
*2026-10-01 10:53Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': True, 'k_atr': 4.0, 'n': 96}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.8666666666666667, "oos_sharpe": 2.0037370325658537, "oos_sortino": 3.362026857010322, "oos_mdd": 0.21088808730186026, "oos_net_return": 2.6801064223360416, "oos_trades": 229, "oos_profit_factor": 2.2287075749563208, "distinct_param_sets_chosen": 6, "median_train_sharpe": 3.159192999454817}

gates: {"wfo_sharpe": [2.0037370325658537, 0.8, true], "wfo_positive_windows": [0.8666666666666667, 0.5, true], "research_trades": [278.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed0] research: meanrev
*2026-10-01 10:53Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 3.0, 'lookback': 24, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.4, "oos_sharpe": -0.7629897757683688, "oos_sortino": -1.134531732129589, "oos_mdd": 0.2876098815560665, "oos_net_return": -0.2458530194161932, "oos_trades": 267, "oos_profit_factor": 0.8141054679244285, "distinct_param_sets_chosen": 7, "median_train_sharpe": 0.07689096608848112}

gates: {"wfo_sharpe": [-0.7629897757683688, 0.8, false], "wfo_positive_windows": [0.4, 0.5, false], "research_trades": [163.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-planted-seed0] research: squeeze
*2026-10-01 10:53Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 4.0, 'lookback': 24, 'quantile': 0.1}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.7333333333333333, "oos_sharpe": 1.234765446424805, "oos_sortino": 2.316973883362301, "oos_mdd": 0.12160079926326917, "oos_net_return": 0.7189118358835769, "oos_trades": 557, "oos_profit_factor": 1.3277581921944137, "distinct_param_sets_chosen": 5, "median_train_sharpe": 1.6309063122524392}

gates: {"wfo_sharpe": [1.234765446424805, 0.8, true], "wfo_positive_windows": [0.7333333333333333, 0.5, true], "research_trades": [565.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed0] research: ml_gbm
*2026-10-01 10:54Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.03, 'horizon': 24, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.5333333333333333, "oos_sharpe": 0.8584291232720933, "oos_sortino": 1.5066307734686093, "oos_mdd": 0.3402869680963051, "oos_net_return": 0.8523675684684013, "oos_trades": 745, "oos_profit_factor": 1.190351752481581, "distinct_param_sets_chosen": 5, "median_train_sharpe": 0.8744145168690315}

gates: {"wfo_sharpe": [0.8584291232720933, 0.8, true], "wfo_positive_windows": [0.5333333333333333, 0.5, true], "research_trades": [723.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed0] HOLD-OUT: donchian
*2026-10-01 10:54Z*

params `{'allow_short': True, 'k_atr': 4.0, 'n': 96}`: net=0.726 sharpe=1.58 sortino=2.68 mdd=0.143 pf=1.68 trades=144; DSR=0.921 (strict 0.006); **accepted=False**


### [synthetic-planted-seed0] HOLD-OUT: squeeze
*2026-10-01 10:54Z*

params `{'k_atr': 4.0, 'lookback': 24, 'quantile': 0.1}`: net=0.314 sharpe=1.37 sortino=2.68 mdd=0.069 pf=1.41 trades=251; DSR=0.869 (strict 0.001); **accepted=False**


### [synthetic-planted-seed0] HOLD-OUT: ml_gbm
*2026-10-01 10:55Z*

params `{'delta': 0.03, 'horizon': 24, 'k_atr': 3.0}`: net=0.386 sharpe=0.79 sortino=1.27 mdd=0.160 pf=1.15 trades=400; DSR=0.573 (strict 0.000); **accepted=False**
