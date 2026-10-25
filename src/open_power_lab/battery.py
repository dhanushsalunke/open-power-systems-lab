"""Software-only equivalent-circuit battery model.

Current sign convention: positive current discharges the battery; negative
current charges it. All quantities use SI units except capacity in ampere-hours.
"""

from dataclasses import dataclass
import numpy as np


class BatteryValidityError(ValueError):
    """Raised when a battery input or operating condition is invalid."""


@dataclass(frozen=True)
class BatteryConfig:
    capacity_ah: float
    nominal_voltage_v: float
    initial_soc: float
    internal_resistance_ohm: float
    coulombic_efficiency: float = 0.995
    charge_efficiency: float = 0.98
    discharge_efficiency: float = 0.98
    minimum_soc: float = 0.0
    maximum_soc: float = 1.0
    maximum_discharge_current_a: float = 10.0
    maximum_charge_current_a: float = 5.0
    ocv_soc_points: tuple[float, ...] = (0.0, 0.2, 0.5, 0.8, 1.0)
    ocv_voltage_points: tuple[float, ...] = (3.0, 3.45, 3.7, 3.9, 4.2)

    def validate(self) -> None:
        if (
            self.capacity_ah <= 0
            or self.nominal_voltage_v <= 0
            or self.internal_resistance_ohm < 0
        ):
            raise BatteryValidityError(
                "capacity, nominal voltage, and resistance are invalid"
            )
        if not self.minimum_soc <= self.initial_soc <= self.maximum_soc:
            raise BatteryValidityError("initial SOC is outside configured limits")
        if (
            not 0 < self.coulombic_efficiency <= 1
            or not 0 < self.charge_efficiency <= 1
            or not 0 < self.discharge_efficiency <= 1
        ):
            raise BatteryValidityError("efficiencies must be in (0, 1]")
        if (
            len(self.ocv_soc_points) != len(self.ocv_voltage_points)
            or len(self.ocv_soc_points) < 2
        ):
            raise BatteryValidityError(
                "OCV lookup points must have equal length and at least two points"
            )
        if any(b <= a for a, b in zip(self.ocv_soc_points, self.ocv_soc_points[1:])):
            raise BatteryValidityError("OCV SOC points must be strictly increasing")
        if (
            self.ocv_soc_points[0] > self.minimum_soc
            or self.ocv_soc_points[-1] < self.maximum_soc
        ):
            raise BatteryValidityError("OCV lookup must cover the configured SOC range")


@dataclass
class BatteryState:
    soc: float
    terminal_voltage_v: float
    current_a: float = 0.0
    temperature_c: float = 25.0


class TheveninBattery:
    """First-order electrical battery model with a static OCV-SOC curve."""

    def __init__(self, config: BatteryConfig):
        config.validate()
        self.config = config
        self.state = BatteryState(
            config.initial_soc, self.open_circuit_voltage(config.initial_soc)
        )

    def open_circuit_voltage(self, soc: float) -> float:
        if not self.config.minimum_soc <= soc <= self.config.maximum_soc:
            raise BatteryValidityError("SOC is outside configured limits")
        return float(
            np.interp(soc, self.config.ocv_soc_points, self.config.ocv_voltage_points)
        )

    def step(self, current_a: float, dt_s: float) -> dict[str, float]:
        c = self.config
        if dt_s <= 0 or not np.isfinite(current_a):
            raise BatteryValidityError("timestep must be positive and current finite")
        if (
            current_a > c.maximum_discharge_current_a
            or current_a < -c.maximum_charge_current_a
        ):
            raise BatteryValidityError(
                "requested current exceeds configured current limit"
            )
        efficiency = (
            c.discharge_efficiency
            if current_a >= 0
            else c.coulombic_efficiency * c.charge_efficiency
        )
        soc_delta = -current_a * dt_s / (3600.0 * c.capacity_ah)
        soc_delta = soc_delta / efficiency if current_a >= 0 else soc_delta * efficiency
        soc_next = self.state.soc + soc_delta
        if soc_next < c.minimum_soc - 1e-12 or soc_next > c.maximum_soc + 1e-12:
            raise BatteryValidityError("requested current would exceed SOC limits")
        soc_next = min(c.maximum_soc, max(c.minimum_soc, soc_next))
        ocv = self.open_circuit_voltage(soc_next)
        terminal = ocv - current_a * c.internal_resistance_ohm
        if terminal <= 0:
            raise BatteryValidityError("terminal voltage became nonpositive")
        self.state = BatteryState(
            soc_next, terminal, current_a, self.state.temperature_c
        )
        return {
            "soc": soc_next,
            "ocv_v": ocv,
            "terminal_voltage_v": terminal,
            "current_a": current_a,
            "electrical_power_w": terminal * current_a,
            "stored_energy_j": soc_next * c.capacity_ah * 3600.0 * c.nominal_voltage_v,
        }
