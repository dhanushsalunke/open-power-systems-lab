from dataclasses import dataclass
import math
from .config import PlantConfig

@dataclass
class PlantState:
    inductor_current_a: float = 0.0
    capacitor_voltage_v: float = 0.0
    temperature_c: float = 25.0

class AveragedBuck:
    """Continuous-conduction averaged buck model using SI units.

    di/dt = (d*Vin - Vout - i*R_L - d*I*R_sw)/L
    dV/dt = (i - Vout/Rload)/C
    """
    def __init__(self, config: PlantConfig):
        self.config = config
        self.state = PlantState()

    def step(self, duty: float, input_v: float, load_r: float, dt: float) -> dict[str, float]:
        p = self.config
        duty = min(1.0, max(0.0, duty))
        i = max(0.0, self.state.inductor_current_a)
        v = max(0.0, self.state.capacitor_voltage_v)
        effective_load = max(0.01, load_r)
        di = (duty * input_v - v - i * p.inductor_resistance_ohm - duty * i * p.switch_resistance_ohm) / p.inductance_h
        dv = (i - v / effective_load) / p.capacitance_f
        i_next = max(0.0, i + dt * di)
        v_next = max(0.0, v + dt * dv)
        conduction_loss = i_next * i_next * (p.inductor_resistance_ohm + duty * p.switch_resistance_ohm)
        diode_loss = max(0.0, (1.0 - duty) * i_next * p.diode_drop_v)
        self.state = PlantState(i_next, v_next, 25.0 + (conduction_loss + diode_loss) * p.thermal_resistance_c_per_w)
        input_power = max(0.0, input_v * duty * i_next)
        output_power = v_next * v_next / effective_load
        return {"inductor_current_a": i_next, "output_voltage_v": v_next, "input_power_w": input_power,
                "output_power_w": output_power, "conduction_loss_w": conduction_loss,
                "diode_loss_w": diode_loss, "temperature_c": self.state.temperature_c}

    def equilibrium_duty(self, input_v: float | None = None) -> float:
        vin = input_v or self.config.input_voltage_v
        return min(1.0, max(0.0, (self.config.reference_voltage_v + self.config.diode_drop_v * 0.05) / vin))

    def small_signal_poles(self, load_r: float | None = None) -> tuple[complex, complex]:
        p = self.config
        r = load_r or p.load_resistance_ohm
        a = p.inductor_resistance_ohm
        b = 1.0 / r
        disc = (a / p.inductance_h + b / p.capacitance_f) ** 2 - 4.0 / (p.inductance_h * p.capacitance_f)
        root = complex(disc) ** 0.5
        center = -(a / p.inductance_h + b / p.capacitance_f) / 2.0
        return center + root / 2.0, center - root / 2.0
