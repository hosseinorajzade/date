"""Transaction-cost model. All rates are fractions of notional, per side."""
from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class CostModel:
    fee_bps: float = 5.0
    slippage_bps: float = 3.0
    stop_extra_slippage_bps: float = 3.0
    funding_bps_per_8h: float = 1.0  # fallback only; real funding series is passed to the engine

    @property
    def fee(self) -> float:
        return self.fee_bps * 1e-4

    @property
    def slip(self) -> float:
        return self.slippage_bps * 1e-4

    @property
    def stop_slip(self) -> float:
        return (self.slippage_bps + self.stop_extra_slippage_bps) * 1e-4

    def stressed(self, mult: float) -> "CostModel":
        """Scale fees and slippage (NOT funding, which is a market quantity) by `mult`."""
        return replace(self, fee_bps=self.fee_bps * mult, slippage_bps=self.slippage_bps * mult,
                       stop_extra_slippage_bps=self.stop_extra_slippage_bps * mult)

    @property
    def round_trip_bps(self) -> float:
        return 2 * (self.fee_bps + self.slippage_bps)

    @classmethod
    def from_config(cls, cfg: dict) -> "CostModel":
        c = cfg["costs"]
        return cls(c["fee_bps"], c["slippage_bps"], c["stop_extra_slippage_bps"], c["funding_bps_per_8h"])
