from dataclasses import dataclass
from .config import InitialConditions, PlantConfig


class ModelValidityError(ValueError):
    """Raised when a state leaves the declared averaged-model operating region."""


@dataclass
class PlantState:
    inductor_current_a: float = 0.0
    capacitor_voltage_v: float = 0.0
    temperature_c: float = 25.0


class AveragedBuck:
    """Continuous-conduction averaged buck model using SI units.

    di/dt = (d*Vin - (1-d)*V_diode - Vout - i*R_L - d*i*R_sw)/L
    dV/dt = (i - Vout/Rload)/C
    """

    def __init__(self, config: PlantConfig, initial: InitialConditions | None = None):
        self.config = config
        initial = initial or InitialConditions()
        self.state = PlantState(
            initial.inductor_current_a, initial.output_voltage_v, initial.temperature_c
        )

    def step(
        self, duty: float, input_v: float, load_r: float, dt: float
    ) -> dict[str, float]:
        p = self.config
        if not 0.0 <= duty <= 1.0 or input_v <= 0.0 or load_r <= 0.0 or dt <= 0.0:
            raise ModelValidityError(
                "duty, input voltage, load resistance, and timestep must be physical"
            )
        duty = float(duty)
        i = self.state.inductor_current_a
        v = self.state.capacitor_voltage_v
        effective_load = load_r
        diode_voltage = (1.0 - duty) * p.diode_drop_v
        di = (
            duty * input_v
            - diode_voltage
            - v
            - i * p.inductor_resistance_ohm
            - duty * i * p.switch_resistance_ohm
        ) / p.inductance_h
        dv = (i - v / effective_load) / p.capacitance_f
        i_next = i + dt * di
        v_next = v + dt * dv
        if not all(map(lambda x: x == x and abs(x) < 1e12, (i_next, v_next))):
            raise ModelValidityError("non-finite or divergent converter state")
        if i_next < -1e-9 and p.conduction_mode == "ccm":
            raise ModelValidityError(
                "CCM model crossed the zero-current boundary; reduce timestep or use a DCM model"
            )
        if v_next < -1e-9:
            raise ModelValidityError("converter output voltage became negative")
        i_next = max(0.0, i_next)
        v_next = max(0.0, v_next)
        conduction_loss = (
            i_next
            * i_next
            * (p.inductor_resistance_ohm + duty * p.switch_resistance_ohm)
        )
        diode_loss = max(0.0, (1.0 - duty) * i_next * p.diode_drop_v)
        self.state = PlantState(
            i_next,
            v_next,
            25.0 + (conduction_loss + diode_loss) * p.thermal_resistance_c_per_w,
        )
        input_power = max(0.0, input_v * duty * i_next)
        output_power = v_next * v_next / effective_load
        return {
            "inductor_current_a": i_next,
            "output_voltage_v": v_next,
            "input_power_w": input_power,
            "output_power_w": output_power,
            "conduction_loss_w": conduction_loss,
            "diode_loss_w": diode_loss,
            "temperature_c": self.state.temperature_c,
        }

    def equilibrium_duty(self, input_v: float | None = None) -> float:
        vin = input_v or self.config.input_voltage_v
        if vin <= 0:
            raise ModelValidityError("input voltage must be positive")
        # Averaged buck balance including the configured off-state diode drop.
        return min(
            1.0,
            max(
                0.0,
                (self.config.reference_voltage_v + self.config.diode_drop_v)
                / (vin + self.config.diode_drop_v),
            ),
        )

    def small_signal_poles(
        self, load_r: float | None = None
    ) -> tuple[complex, complex]:
        p = self.config
        r = load_r or p.load_resistance_ohm
        a = p.inductor_resistance_ohm
        b = 1.0 / r
        disc = (a / p.inductance_h + b / p.capacitance_f) ** 2 - 4.0 / (
            p.inductance_h * p.capacitance_f
        )
        root = complex(disc) ** 0.5
        center = -(a / p.inductance_h + b / p.capacitance_f) / 2.0
        return center + root / 2.0, center - root / 2.0
