from __future__ import annotations

from .base import Strategy
from .meanrev import ZScoreMeanReversion
from .ml import GBMDirectional
from .squeeze import SqueezeBreakout
from .trend import DonchianTrend

FAMILIES: dict[str, type[Strategy]] = {
    c.name: c for c in (DonchianTrend, ZScoreMeanReversion, SqueezeBreakout, GBMDirectional)
}


def get_family(name: str) -> type[Strategy]:
    return FAMILIES[name]


def make(name: str, **params) -> Strategy:
    return FAMILIES[name](**params)
