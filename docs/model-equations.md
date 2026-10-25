# Model equations and limits

For the averaged buck converter in continuous conduction:

`L di/dt = d Vin - Vo - i R_L - d i R_SW`

`C dVo/dt = i - Vo/Rload`

The controller is a discrete PI controller with duty saturation and conditional anti-windup. Input power is approximated as `Vin * d * i`; output power is `Vo²/Rload`. Conduction and diode losses are estimated for an engineering trend, not a switching-loss or thermal-certification model.

Valid first-use range: low-voltage DC, positive L/C/load, duty between configured bounds, and continuous-conduction operation. Discontinuous conduction, startup soft-start, magnetic saturation, switching ripple, gate-drive dead-time, detailed semiconductor behavior, parasitic layout effects, and thermal transients are outside this model.
