import numpy as np
from open_power_lab.analysis import (
    compare_scenarios,
    frequency_response,
    monte_carlo,
    parameter_sweep,
    stability_margin,
)
from open_power_lab.config import load_config


def test_frequency_response_and_margin_are_finite():
    cfg = load_config("configs/baseline.yaml")
    response = frequency_response(cfg, np.logspace(1, 4, 20))
    assert np.isfinite(response["magnitude_db"]).all()
    margin = stability_margin(cfg)
    assert margin["gain_crossover_hz"] is not None


def test_sweep_and_monte_carlo_are_reproducible():
    cfg = load_config("configs/baseline.yaml")
    sweep = parameter_sweep(cfg, "load_resistance_ohm", [4.0, 5.0])
    assert len(sweep) == 2 and sweep[0]["peak_current_a"] > 0
    assert monte_carlo(cfg, "inductance_h", 470e-6, 0.02, 4) == monte_carlo(
        cfg, "inductance_h", 470e-6, 0.02, 4
    )


def test_fault_comparison_reports_delta():
    cfg = load_config("configs/baseline.yaml")
    comparison = compare_scenarios(cfg)
    assert set(comparison) == {"baseline", "faulted", "delta"}
    assert "load_step" in comparison["faulted"]["fault_events"]
