from dataclasses import dataclass
import numpy as np
from .config import SystemConfig
from .models import AveragedBuck
from .control import PIController
from .faults import FaultInjector

@dataclass
class SimulationResult:
    data: dict[str, np.ndarray]
    summary: object | None = None

def run(config: SystemConfig) -> SimulationResult:
    n = int(round(config.simulation.duration_s / config.simulation.timestep_s)) + 1
    t = np.linspace(0.0, config.simulation.duration_s, n)
    plant = AveragedBuck(config.plant)
    controller = PIController(config.controller)
    injector = FaultInjector(config.faults, config.simulation.seed)
    out = {key: np.zeros(n) for key in ("output_voltage_v", "inductor_current_a", "input_power_w", "output_power_w", "conduction_loss_w", "diode_loss_w", "temperature_c", "duty", "measured_voltage_v", "load_resistance_ohm", "input_voltage_v")}
    faults: list[str] = [""] * n
    for k, time_s in enumerate(t):
        measured_prev = out["output_voltage_v"][k - 1] if k else 0.0
        effects = injector.apply(float(time_s), config.plant.input_voltage_v, config.plant.load_resistance_ohm, measured_prev)
        measured = effects.measured_voltage_v
        if measured is None:
            controller.reset()
            duty, saturated = config.controller.duty_min, True
        else:
            duty, saturated = controller.step(config.plant.reference_voltage_v, measured, config.simulation.timestep_s)
        duty *= effects.actuator_scale
        values = plant.step(duty, effects.input_voltage_v, effects.load_resistance_ohm, config.simulation.timestep_s)
        for key, value in values.items(): out[key][k] = value
        out["duty"][k] = duty
        out["measured_voltage_v"][k] = values["output_voltage_v"] if measured is None else measured
        out["load_resistance_ohm"][k] = effects.load_resistance_ohm
        out["input_voltage_v"][k] = effects.input_voltage_v
        faults[k] = ",".join(effects.fault_active)
    out["time_s"] = t
    out["faults"] = np.asarray(faults, dtype=object)
    return SimulationResult(out)
