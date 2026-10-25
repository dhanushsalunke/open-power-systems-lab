from dataclasses import dataclass
from .config import ControllerConfig

@dataclass
class PIController:
    config: ControllerConfig
    integral: float = 0.0

    def reset(self) -> None:
        self.integral = 0.0

    def step(self, reference: float, measurement: float, dt: float) -> tuple[float, bool]:
        error = reference - measurement
        proposed = self.config.kp * error + self.integral
        saturated = proposed < self.config.duty_min or proposed > self.config.duty_max
        output = min(self.config.duty_max, max(self.config.duty_min, proposed))
        if not saturated or (output == self.config.duty_min and error > 0) or (output == self.config.duty_max and error < 0):
            self.integral += self.config.ki * error * dt
        output = min(self.config.duty_max, max(self.config.duty_min, self.config.kp * error + self.integral))
        return output, saturated
