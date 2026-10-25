from open_power_lab.config import load_config
from open_power_lab.simulation import run
from open_power_lab.diagnostics import evaluate

def test_baseline_closed_loop_and_fault_are_deterministic():
    cfg = load_config("configs/baseline.yaml")
    first = run(cfg).data
    second = run(cfg).data
    assert first["output_voltage_v"].tolist() == second["output_voltage_v"].tolist()
    summary = evaluate(first, cfg.plant.reference_voltage_v, cfg.simulation.timestep_s, cfg.plant.current_limit_a)
    assert summary.verdict in {"PASS", "REVIEW"}
    assert "load_step" in summary.fault_events
    assert summary.max_current_a >= 0
