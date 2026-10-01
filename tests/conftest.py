import numpy as np
import pandas as pd
import pytest

from quantbot.backtest.costs import CostModel
from quantbot.backtest.engine import EngineConfig


def make_bars(opens, highs=None, lows=None, closes=None, start="2024-01-01", freq="1h"):
    o = np.asarray(opens, float)
    c = np.asarray(closes if closes is not None else opens, float)
    h = np.asarray(highs if highs is not None else np.maximum(o, c), float)
    l = np.asarray(lows if lows is not None else np.minimum(o, c), float)
    idx = pd.date_range(start, periods=len(o), freq=freq, tz="UTC")
    return pd.DataFrame({"open": o, "high": h, "low": l, "close": c, "volume": 1.0}, index=idx)


@pytest.fixture
def zero_cost_cfg():
    return EngineConfig(costs=CostModel(0, 0, 0, 0), risk_per_trade=0.01, max_leverage=100.0,
                        min_stop_pct=0.0, daily_loss_limit=1.0, kill_switch_drawdown=1.0)


@pytest.fixture
def cost_cfg():
    return EngineConfig(costs=CostModel(5.0, 3.0, 3.0, 0.0), risk_per_trade=0.01, max_leverage=100.0,
                        min_stop_pct=0.0, daily_loss_limit=1.0, kill_switch_drawdown=1.0)
