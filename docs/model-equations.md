# Model equations and limits

For the averaged buck converter in continuous conduction:

`L di/dt = d Vin - (1-d) V_D - Vo - i R_L - d i R_SW`

`C dVo/dt = i - Vo/Rload`

The controller is a discrete PI controller with duty saturation and conditional anti-windup. Input power is approximated as `Vin * d * i`; output power is `Vo²/Rload`. Conduction and diode losses are estimated for an engineering trend, not a switching-loss or thermal-certification model.

Valid first-use range: low-voltage DC, positive L/C/load, duty between configured bounds, and the configured conduction mode. `ccm` fails loudly when the inductor current crosses zero. `dcm_approx` clips the averaged current at zero for startup and light-load exploration; it is not a cycle-by-cycle discontinuous-conduction solution and must not be used for ripple, peak-current, or switch-timing claims. Startup soft-start, magnetic saturation, switching ripple, gate-drive dead-time, detailed semiconductor behavior, parasitic layout effects, and thermal transients are outside this model.
