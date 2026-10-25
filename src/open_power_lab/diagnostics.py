from dataclasses import asdict, dataclass
import numpy as np


@dataclass
class DiagnosticSummary:
    steady_state_error_v: float
    peak_overshoot_v: float
    rms_error_v: float
    rise_time_s: float | None
    settling_time_s: float | None
    max_current_a: float
    max_temperature_c: float
    efficiency_percent: float
    energy_balance_residual_j: float | None
    fault_events: list[str]
    warnings: list[str]
    verdict: str

    def to_dict(self) -> dict:
        return asdict(self)


def _crossing_time(t: np.ndarray, values: np.ndarray, threshold: float) -> float | None:
    indexes = np.flatnonzero(values >= threshold)
    return float(t[indexes[0]]) if len(indexes) else None


def _settling_time(t: np.ndarray, error: np.ndarray, tolerance: float) -> float | None:
    outside = np.flatnonzero(np.abs(error) > tolerance)
    if not len(outside):
        return float(t[0])
    last = int(outside[-1])
    return None if last >= len(t) - 1 else float(t[last + 1])


def evaluate(
    result: dict[str, np.ndarray],
    reference_v: float,
    timestep_s: float,
    current_limit_a: float,
    inductance_h: float | None = None,
    capacitance_f: float | None = None,
) -> DiagnosticSummary:
    t = np.asarray(result["time_s"], dtype=float)
    v = np.asarray(result["output_voltage_v"], dtype=float)
    i = np.asarray(result["inductor_current_a"], dtype=float)
    p_in = np.asarray(result["input_power_w"], dtype=float)
    p_out = np.asarray(result["output_power_w"], dtype=float)
    error = v - reference_v
    tail = v[max(0, len(v) // 5) :]
    warnings: list[str] = []
    max_current = float(np.max(i))
    if max_current > current_limit_a:
        warnings.append(
            f"current limit exceeded: {max_current:.6g} A > {current_limit_a:.6g} A"
        )
    if np.any(~np.isfinite(v)) or np.any(~np.isfinite(i)):
        warnings.append("non-finite signal detected")
    input_energy = float(np.sum(p_in) * timestep_s)
    output_energy = float(np.sum(p_out) * timestep_s)
    losses = float(
        np.sum(result["conduction_loss_w"] + result["diode_loss_w"]) * timestep_s
    )
    stored_delta = None
    if inductance_h is not None and capacitance_f is not None:
        stored_delta = float(
            0.5 * inductance_h * (i[-1] ** 2 - i[0] ** 2)
            + 0.5 * capacitance_f * (v[-1] ** 2 - v[0] ** 2)
        )
    residual = (
        None
        if stored_delta is None
        else input_energy - output_energy - losses - stored_delta
    )
    efficiency = 100.0 * output_energy / input_energy if input_energy > 0 else 0.0
    rise_10 = _crossing_time(t, v, 0.1 * reference_v)
    rise_90 = _crossing_time(t, v, 0.9 * reference_v)
    rise_time = (
        None if rise_10 is None or rise_90 is None else max(0.0, rise_90 - rise_10)
    )
    settling = _settling_time(t, error, max(0.02 * abs(reference_v), 1e-9))
    faults = sorted(
        {part for item in result["faults"] if item for part in item.split(",") if part}
    )
    steady_error = float(np.mean(tail) - reference_v)
    verdict = (
        "PASS"
        if abs(steady_error) < 0.15
        and max_current <= current_limit_a * 1.05
        and not any("non-finite" in x for x in warnings)
        else "REVIEW"
    )
    return DiagnosticSummary(
        steady_error,
        float(max(0.0, np.max(v) - reference_v)),
        float(np.sqrt(np.mean(error * error))),
        rise_time,
        settling,
        max_current,
        float(np.max(result["temperature_c"])),
        efficiency,
        residual,
        faults,
        warnings,
        verdict,
    )
