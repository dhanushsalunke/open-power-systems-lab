from dataclasses import dataclass, asdict
import numpy as np

@dataclass
class DiagnosticSummary:
    steady_state_error_v: float
    peak_overshoot_v: float
    rms_error_v: float
    max_current_a: float
    max_temperature_c: float
    energy_balance_error_j: float
    fault_events: list[str]
    verdict: str

    def to_dict(self):
        return asdict(self)

def evaluate(result: dict[str, np.ndarray], reference_v: float, timestep_s: float, current_limit_a: float) -> DiagnosticSummary:
    v = result["output_voltage_v"]
    i = result["inductor_current_a"]
    p_in = result["input_power_w"]
    p_out = result["output_power_w"]
    tail = v[max(0, len(v) // 5):]
    error = v - reference_v
    balance = float(np.sum(p_in - p_out) * timestep_s)
    faults = sorted(set(x for x in result["faults"] if x))
    verdict = "PASS" if abs(float(np.mean(tail) - reference_v)) < 0.15 and float(np.max(i)) <= current_limit_a * 1.05 else "REVIEW"
    return DiagnosticSummary(float(np.mean(tail) - reference_v), float(max(0.0, np.max(v) - reference_v)), float(np.sqrt(np.mean(error * error))), float(np.max(i)), float(np.max(result["temperature_c"])), balance, faults, verdict)
