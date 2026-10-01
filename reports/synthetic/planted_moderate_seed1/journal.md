

### [synthetic-planted-seed1] research: donchian
*2026-10-01 10:55Z*

chosen (plateau-smoothed research Sharpe): `{'allow_short': True, 'k_atr': 4.0, 'n': 48}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 1.0, "oos_sharpe": 4.104898335531501, "oos_sortino": 9.116267419071947, "oos_mdd": 0.11963896044380928, "oos_net_return": 23.621590957511888, "oos_trades": 289, "oos_profit_factor": 3.161056742114771, "distinct_param_sets_chosen": 10, "median_train_sharpe": 5.330080347391281}

gates: {"wfo_sharpe": [4.104898335531501, 0.8, true], "wfo_positive_windows": [1.0, 0.5, true], "research_trades": [474.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed1] research: meanrev
*2026-10-01 10:56Z*

chosen (plateau-smoothed research Sharpe): `{'er_max': 0.35, 'k_atr': 2.0, 'lookback': 24, 'z_in': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.3333333333333333, "oos_sharpe": -1.1138090659345699, "oos_sortino": -1.5855421657174376, "oos_mdd": 0.38473778148311755, "oos_net_return": -0.304902965687068, "oos_trades": 178, "oos_profit_factor": 0.6796189700768266, "distinct_param_sets_chosen": 7, "median_train_sharpe": 0.07353686174793017}

gates: {"wfo_sharpe": [-1.1138090659345699, 0.8, false], "wfo_positive_windows": [0.3333333333333333, 0.5, false], "research_trades": [173.0, 100, true], "sensitivity_neighbours_positive": [0.0, 0.6, false]}

**gate verdict: FAIL -> hold-out not touched**


### [synthetic-planted-seed1] research: squeeze
*2026-10-01 10:56Z*

chosen (plateau-smoothed research Sharpe): `{'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 0.9333333333333333, "oos_sharpe": 3.6445056465393244, "oos_sortino": 8.202186685169478, "oos_mdd": 0.07105461494197474, "oos_net_return": 4.881282543159254, "oos_trades": 480, "oos_profit_factor": 2.316391026174659, "distinct_param_sets_chosen": 2, "median_train_sharpe": 3.7283408301667538}

gates: {"wfo_sharpe": [3.6445056465393244, 0.8, true], "wfo_positive_windows": [0.9333333333333333, 0.5, true], "research_trades": [400.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed1] research: ml_gbm
*2026-10-01 10:56Z*

chosen (plateau-smoothed research Sharpe): `{'delta': 0.06, 'horizon': 24, 'k_atr': 3.0}`

walk-forward OOS: {"n_windows": 15, "positive_window_share": 1.0, "oos_sharpe": 4.590530934985268, "oos_sortino": 9.402707069287494, "oos_mdd": 0.1294543750813576, "oos_net_return": 55.48721631255384, "oos_trades": 636, "oos_profit_factor": 2.6384864415133364, "distinct_param_sets_chosen": 3, "median_train_sharpe": 4.544912458225179}

gates: {"wfo_sharpe": [4.590530934985268, 0.8, true], "wfo_positive_windows": [1.0, 0.5, true], "research_trades": [492.0, 100, true], "sensitivity_neighbours_positive": [1.0, 0.6, true]}

**gate verdict: PASS -> hold-out eligible**


### [synthetic-planted-seed1] HOLD-OUT: donchian
*2026-10-01 10:56Z*

params `{'allow_short': True, 'k_atr': 4.0, 'n': 48}`: net=7.114 sharpe=4.82 sortino=9.98 mdd=0.125 pf=2.46 trades=239; DSR=1.000 (strict 0.000); **accepted=True**


### [synthetic-planted-seed1] HOLD-OUT: squeeze
*2026-10-01 10:56Z*

params `{'k_atr': 4.0, 'lookback': 48, 'quantile': 0.2}`: net=1.088 sharpe=2.61 sortino=5.32 mdd=0.087 pf=1.96 trades=208; DSR=1.000 (strict 0.000); **accepted=True**


### [synthetic-planted-seed1] HOLD-OUT: ml_gbm
*2026-10-01 10:58Z*

params `{'delta': 0.06, 'horizon': 24, 'k_atr': 3.0}`: net=11.885 sharpe=4.63 sortino=9.56 mdd=0.222 pf=2.25 trades=267; DSR=1.000 (strict 0.000); **accepted=False**
