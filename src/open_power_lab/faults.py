from dataclasses import dataclass
import numpy as np
from .config import FaultConfig


@dataclass
class FaultEffects:
    input_voltage_v: float
    load_resistance_ohm: float
    measured_voltage_v: float | None
    actuator_scale: float
    fault_active: list[str]


class FaultInjector:
    def __init__(self, faults: tuple[FaultConfig, ...], seed: int):
        self.faults = faults
        self.rng = np.random.default_rng(seed)

    def apply(
        self, time_s: float, input_v: float, load_r: float, true_v: float
    ) -> FaultEffects:
        v, r, scale = input_v, load_r, 1.0
        measured: float | None = true_v
        active: list[str] = []
        for fault in self.faults:
            if time_s < fault.time_s or (
                fault.duration_s is not None
                and time_s >= fault.time_s + fault.duration_s
            ):
                continue
            active.append(fault.type)
            if fault.type == "load_step":
                r = max(0.05, fault.value)
            elif fault.type == "input_step":
                v = fault.value
            elif fault.type == "sensor_bias" and measured is not None:
                measured += fault.value
            elif fault.type == "sensor_noise" and measured is not None:
                measured += float(self.rng.normal(0.0, abs(fault.value)))
            elif fault.type == "sensor_disconnect":
                measured = None
            elif fault.type == "actuator_saturation":
                scale = min(1.0, max(0.0, fault.value))
        return FaultEffects(v, r, measured, scale, active)
