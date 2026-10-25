from dataclasses import replace
import numpy as np
from open_power_lab.config import FaultConfig, load_config
from open_power_lab.simulation import run


def test_timestep_refinement_has_small_final_value_difference():
    cfg = load_config("configs/baseline.yaml")
    fine = replace(
        cfg,
        simulation=replace(cfg.simulation, timestep_s=cfg.simulation.timestep_s / 2),
    )
    coarse_result = run(cfg).data
    fine_result = run(fine).data
    assert (
        abs(
            float(
                coarse_result["output_voltage_v"][-1]
                - fine_result["output_voltage_v"][-1]
            )
        )
        < 0.03
    )


def test_fault_duration_expires_and_seeded_noise_repeats():
    cfg = load_config("configs/baseline.yaml")
    faults = (
        FaultConfig("sensor_bias", 0.1, 0.1, 0.02),
        FaultConfig("sensor_noise", 0.1, 0.01, 0.02),
    )
    cfg = replace(cfg, faults=faults)
    a, b = run(cfg).data, run(cfg).data
    assert np.array_equal(a["output_voltage_v"], b["output_voltage_v"])
    assert any("sensor_bias" in x for x in a["faults"] if x)
    assert a["faults"][-1] == ""
