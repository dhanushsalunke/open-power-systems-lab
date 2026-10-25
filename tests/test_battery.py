import pytest
from open_power_lab.battery import BatteryConfig, BatteryValidityError, TheveninBattery


def battery() -> TheveninBattery:
    return TheveninBattery(BatteryConfig(2.0, 3.7, 0.5, 0.05))


def test_coulomb_counting_discharge_is_analytical():
    model = battery()
    result = model.step(1.0, 360.0)
    assert result["soc"] == pytest.approx(0.4489795918367347, abs=1e-12)
    assert result["terminal_voltage_v"] < result["ocv_v"]


def test_charge_and_discharge_have_expected_signs():
    model = battery()
    before = model.state.soc
    model.step(-1.0, 60.0)
    assert model.state.soc > before


def test_battery_rejects_current_limit_and_soc_violation():
    model = battery()
    with pytest.raises(BatteryValidityError, match="current limit"):
        model.step(11.0, 1.0)
    with pytest.raises(BatteryValidityError, match="SOC limits"):
        model.step(1.0, 4000.0)
