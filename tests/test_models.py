import math
import pytest
from open_power_lab.config import PlantConfig, ControllerConfig, SimulationConfig, SystemConfig
from open_power_lab.models import AveragedBuck

def plant():
    return PlantConfig(12, 5, 470e-6, 100e-6, 0.08, 0.06, 0.55, 5, 3, 18)

def test_equilibrium_duty_is_dimensionless_and_reasonable():
    duty = AveragedBuck(plant()).equilibrium_duty()
    assert 0.4 < duty < 0.5

def test_plant_rejects_bad_parameters():
    with pytest.raises(ValueError):
        SystemConfig(SimulationConfig(1, 2), plant(), ControllerConfig(1, 1, 0, 1)).validate()

def test_energy_values_are_nonnegative():
    model = AveragedBuck(plant())
    out = model.step(0.42, 12, 5, 1e-6)
    assert out["input_power_w"] >= out["output_power_w"] >= 0
