from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import yaml

@dataclass(frozen=True)
class SimulationConfig:
    duration_s: float
    timestep_s: float
    seed: int = 1

@dataclass(frozen=True)
class PlantConfig:
    input_voltage_v: float
    reference_voltage_v: float
    inductance_h: float
    capacitance_f: float
    inductor_resistance_ohm: float
    switch_resistance_ohm: float
    diode_drop_v: float
    load_resistance_ohm: float
    current_limit_a: float
    thermal_resistance_c_per_w: float

@dataclass(frozen=True)
class ControllerConfig:
    kp: float
    ki: float
    duty_min: float
    duty_max: float

@dataclass(frozen=True)
class FaultConfig:
    type: str
    time_s: float
    value: float = 0.0

@dataclass(frozen=True)
class SystemConfig:
    simulation: SimulationConfig
    plant: PlantConfig
    controller: ControllerConfig
    faults: tuple[FaultConfig, ...] = field(default_factory=tuple)

    def validate(self) -> None:
        if self.simulation.duration_s <= 0 or self.simulation.timestep_s <= 0:
            raise ValueError("simulation duration and timestep must be positive")
        if self.simulation.timestep_s > self.simulation.duration_s:
            raise ValueError("timestep cannot exceed duration")
        p = self.plant
        if min(p.input_voltage_v, p.inductance_h, p.capacitance_f, p.load_resistance_ohm) <= 0:
            raise ValueError("input voltage, L, C, and load resistance must be positive")
        if p.current_limit_a <= 0 or p.thermal_resistance_c_per_w <= 0:
            raise ValueError("current limit and thermal resistance must be positive")
        c = self.controller
        if c.kp < 0 or c.ki < 0 or not 0 <= c.duty_min < c.duty_max <= 1:
            raise ValueError("invalid controller gains or duty limits")
        allowed = {"load_step", "input_step", "sensor_bias", "sensor_noise", "sensor_disconnect", "actuator_saturation"}
        unknown = {f.type for f in self.faults} - allowed
        if unknown:
            raise ValueError(f"unsupported faults: {sorted(unknown)}")

def load_config(path: str | Path) -> SystemConfig:
    raw: dict[str, Any] = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    cfg = SystemConfig(
        simulation=SimulationConfig(**raw["simulation"]),
        plant=PlantConfig(**raw["plant"]),
        controller=ControllerConfig(**raw["controller"]),
        faults=tuple(FaultConfig(**fault) for fault in raw.get("faults", [])),
    )
    cfg.validate()
    return cfg
