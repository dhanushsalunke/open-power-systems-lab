from dataclasses import replace
import numpy as np
from .config import SystemConfig
from .models import AveragedBuck
from .simulation import run

def frequency_response(config: SystemConfig, frequencies_hz: np.ndarray) -> dict[str, np.ndarray]:
    """Return duty-to-output small-signal response of the averaged buck plant."""
    p = config.plant
    r = p.load_resistance_ohm
    A = np.array([[-(p.inductor_resistance_ohm + p.switch_resistance_ohm * 0.5) / p.inductance_h, -1 / p.inductance_h],
                  [1 / p.capacitance_f, -1 / (r * p.capacitance_f)]], dtype=float)
    B = np.array([[p.input_voltage_v / p.inductance_h], [0.0]])
    C = np.array([[0.0, 1.0]])
    plant = np.empty(len(frequencies_hz), dtype=complex)
    loop = np.empty(len(frequencies_hz), dtype=complex)
    for idx, frequency in enumerate(frequencies_hz):
        jw = 2j * np.pi * frequency
        plant[idx] = (C @ np.linalg.solve(jw * np.eye(2) - A, B))[0, 0]
        controller = config.controller.kp + config.controller.ki / jw
        loop[idx] = plant[idx] * controller
    return {"frequency_hz": np.asarray(frequencies_hz), "plant": plant, "loop": loop,
            "magnitude_db": 20 * np.log10(np.maximum(np.abs(loop), 1e-15)), "phase_deg": np.angle(loop, deg=True)}

def stability_margin(config: SystemConfig, frequencies_hz: np.ndarray | None = None) -> dict[str, float | None]:
    frequencies_hz = frequencies_hz if frequencies_hz is not None else np.logspace(0, 5, 1200)
    response = frequency_response(config, frequencies_hz)
    magnitude = response["magnitude_db"]
    crossings = np.where(np.diff(np.sign(magnitude)) != 0)[0]
    if len(crossings) == 0:
        return {"gain_crossover_hz": None, "phase_margin_deg": None}
    idx = int(crossings[0])
    phase_margin = 180.0 + float(response["phase_deg"][idx])
    return {"gain_crossover_hz": float(response["frequency_hz"][idx]), "phase_margin_deg": phase_margin}

def parameter_sweep(config: SystemConfig, parameter: str, values: list[float]) -> list[dict]:
    rows = []
    for value in values:
        if not hasattr(config.plant, parameter):
            raise ValueError(f"unknown plant parameter: {parameter}")
        candidate = replace(config, plant=replace(config.plant, **{parameter: value}))
        result = run(candidate).data
        rows.append({"parameter": parameter, "value": value, "peak_current_a": float(np.max(result["inductor_current_a"])),
                     "final_voltage_v": float(result["output_voltage_v"][-1]), "max_temperature_c": float(np.max(result["temperature_c"]))})
    return rows

def monte_carlo(config: SystemConfig, parameter: str, nominal: float, relative_sigma: float, samples: int = 20) -> list[dict]:
    rng = np.random.default_rng(config.simulation.seed)
    values = rng.normal(nominal, abs(nominal * relative_sigma), samples)
    return parameter_sweep(config, parameter, [float(max(1e-12, x)) for x in values])
