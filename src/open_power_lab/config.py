from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import yaml


@dataclass(frozen=True)
class SimulationConfig:
    duration_s: float
    timestep_s: float
    seed: int = 1
    output_decimation: int = 1


@dataclass(frozen=True)
class InitialConditions:
    inductor_current_a: float = 0.0
    output_voltage_v: float = 0.0
    temperature_c: float = 25.0


@dataclass(frozen=True)
class SolverConfig:
    method: str = "forward_euler"
    max_state_abs: float = 1.0e6
    fail_on_ccm_boundary: bool = True


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
    conduction_mode: str = "ccm"


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
    duration_s: float | None = None


@dataclass(frozen=True)
class SystemConfig:
    simulation: SimulationConfig
    plant: PlantConfig
    controller: ControllerConfig
    initial_conditions: InitialConditions = field(default_factory=InitialConditions)
    solver: SolverConfig = field(default_factory=SolverConfig)
    faults: tuple[FaultConfig, ...] = field(default_factory=tuple)

    def validate(self) -> None:
        if self.simulation.duration_s <= 0 or self.simulation.timestep_s <= 0:
            raise ValueError("simulation duration and timestep must be positive")
        if self.simulation.timestep_s > self.simulation.duration_s:
            raise ValueError("timestep cannot exceed duration")
        if self.simulation.output_decimation < 1:
            raise ValueError("output_decimation must be at least 1")
        p = self.plant
        if (
            min(
                p.input_voltage_v,
                p.inductance_h,
                p.capacitance_f,
                p.load_resistance_ohm,
            )
            <= 0
        ):
            raise ValueError(
                "input voltage, L, C, and load resistance must be positive"
            )
        if p.current_limit_a <= 0 or p.thermal_resistance_c_per_w <= 0:
            raise ValueError("current limit and thermal resistance must be positive")
        if p.conduction_mode not in {"ccm", "dcm_approx"}:
            raise ValueError("conduction_mode must be ccm or dcm_approx")
        ic = self.initial_conditions
        if (
            min(ic.inductor_current_a, ic.output_voltage_v) < 0
            or ic.temperature_c < -273.15
        ):
            raise ValueError(
                "initial current/voltage must be nonnegative and temperature must be physical"
            )
        if self.solver.method != "forward_euler" or self.solver.max_state_abs <= 0:
            raise ValueError("unsupported solver or invalid max_state_abs")
        c = self.controller
        if c.kp < 0 or c.ki < 0 or not 0 <= c.duty_min < c.duty_max <= 1:
            raise ValueError("invalid controller gains or duty limits")
        allowed = {
            "load_step",
            "input_step",
            "sensor_bias",
            "sensor_noise",
            "sensor_disconnect",
            "actuator_saturation",
        }
        unknown = {f.type for f in self.faults} - allowed
        if unknown:
            raise ValueError(f"unsupported faults: {sorted(unknown)}")
        for fault in self.faults:
            if fault.time_s < 0 or (
                fault.duration_s is not None and fault.duration_s <= 0
            ):
                raise ValueError(
                    "fault times must be nonnegative and durations positive"
                )


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
