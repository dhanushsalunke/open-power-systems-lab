# Open Power Systems Lab

Open Power Systems Lab is a modular, reproducible engineering platform for investigating low-voltage power converters, control loops, measurement chains, faults, and hardware-in-the-loop interfaces before hardware is built.

The first release contains a complete vertical slice: a parameterized averaged buck converter, closed-loop PI control, load and sensor fault injection, diagnostics, CSV/JSON/PNG/Markdown reporting, and a machine-readable JSON-lines protocol for a future microcontroller adapter.

## Quick start

```powershell
py -m pip install -e .
python -m open_power_lab run --config configs/baseline.yaml --output results/baseline
pytest -q
```

The run produces `signals.csv`, `summary.json`, `report.md`, and plots when Matplotlib is installed. No physical hardware is required.

## Implemented status

| Capability | Status |
|---|---|
| Averaged buck plant with losses and thermal estimate | Implemented and unit-tested |
| Closed-loop PI voltage control | Implemented and transient-tested |
| Load step, input variation, sensor bias/noise/disconnect | Implemented and diagnosed |
| Parameter sweep and Monte Carlo hooks | Implemented in the simulation API |
| Frequency response and stability margin estimate | Implemented for the linearized buck model |
| JSON-lines host protocol with validation/timeouts | Implemented and tested offline |
| Firmware state-machine scaffold | Interface scaffold; not flashed or hardware-validated |
| KiCad low-voltage interface source | Reference source; ERC/DRC not run here |
| ngspice, Renode, physical HIL | Optional extension points; not executed in this environment |

Simulation results are not proof of hardware safety. All reports include the model assumptions and validation boundary.

## Architecture

```text
YAML config -> validated system definition -> plant + controller -> faults
                                         |                     |
                                         v                     v
                                  time-series results -> diagnostics
                                         |                     |
                              CSV / JSON / plots / report
                                         |
                                  host protocol -> MCU adapter
```

See `docs/architecture.md`, `docs/model-equations.md`, and `docs/research-notes.md` for design decisions and the comparison with related projects.

## Design boundary

The default model is a continuous-time averaged buck converter. It is appropriate for control-loop and energy-balance studies where switching ripple is not the question. It does not model semiconductor switching losses, EMI, gate-drive timing, layout parasitics, magnetic saturation, or certified protection behavior. Use a switching simulator or measured hardware for those questions.

## License

MIT. Hardware source is included as an engineering reference and must be reviewed against the selected parts, footprints, PCB manufacturer rules, and applicable safety requirements before fabrication.
