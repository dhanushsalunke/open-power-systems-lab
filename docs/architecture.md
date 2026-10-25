# Architecture and acceptance criteria

## Interfaces

- `config.py`: validated YAML to immutable system definitions.
- `models.py`: physical state and averaged converter equations; no UI or file I/O.
- `control.py`: discrete controller state and actuator limits.
- `faults.py`: deterministic scenario transformations with seeded noise.
- `simulation.py`: time integration and signal collection.
- `diagnostics.py`: quantitative acceptance metrics and verdicts.
- `reporting.py`: machine-readable and human-readable evidence.
- `protocol.py`: bounded host/embedded message contract.

## Initial acceptance criteria

1. Configuration rejects nonphysical L, C, load, timing, and controller limits.
2. Baseline run is deterministic for the same seed.
3. Closed-loop steady-state error is reported in volts, not hidden by a plot.
4. Load-step and sensor faults appear in the diagnostic record.
5. Power quantities remain nonnegative and the report labels simulation-only evidence.
6. Malformed protocol messages fail closed.

The analysis module also exposes a linearized frequency response, gain crossover/phase-margin estimate, deterministic parameter sweeps, and seeded Monte Carlo sampling. These are screening tools for the averaged model, not substitutes for switching-level or measured frequency-response work.

The battery module follows the same boundary: it is an independent software model that can later be composed into a bus or energy-management experiment without coupling storage equations to the converter or CLI layers.

The acceptance criteria are software-model criteria. They do not establish component ratings, EMI compliance, or hardware safety.
