# Repository audit — 2026-10-25

## Baseline inspected

- Branch: `master`
- Working tree: clean before this upgrade
- Baseline commit: `125e61b Add baseline reference evidence`
- Baseline tests: 8 passed
- Baseline example: completed with a simulation-only `PASS`
- Environment limitation: ngspice, KiCad, Renode, and physical hardware were not available or exercised

## Existing strengths

- Clear separation between configuration, plant model, controller, fault injector, diagnostics, reporting, protocol, and CLI.
- Deterministic seeded simulation and a reproducible YAML example.
- A documented averaged buck model with an end-to-end report.
- Useful initial protocol and firmware-state-machine extension points.

## Defects and risks found

1. The CLI supported only `run`; configuration validation, model listing, sweeps, verification, and report inspection were not first-class workflows.
2. The plant clamped negative current and voltage to zero. This could hide numerical failure and made invalid operating regions indistinguishable from valid discontinuous-conduction behavior.
3. The model did not declare its conduction-mode boundary, did not detect timestep instability, and had no timestep-sensitivity acceptance test.
4. `diode_drop_v` was used only as a loss term and the duty estimate contained an unexplained `0.05` factor. The revised model makes the approximation explicit and reports mode/validity warnings.
5. Faults were permanent after their start time; duration, expected response, and detection criteria were not represented. Fault injection and diagnostics were coupled only through a string list.
6. Reports omitted the exact configuration, software version, solver settings, initial conditions, warnings, and artifact manifest.
7. Diagnostics lacked rise time, settling time, overshoot, load-step comparison, efficiency, operating margins, and a defined energy-balance residual.
8. The repository retained hardware and firmware reference artifacts even though this software-focused release must not imply verified hardware. They are now explicitly classified as out-of-scope legacy references and are not part of simulation validation.

## Upgrade priorities

1. Add explicit result/status/warning contracts and non-silent numerical validity handling.
2. Add analytical and numerical robustness tests for the plant and controller.
3. Add reusable transient metrics, fault windows, baseline-vs-fault comparisons, and configuration provenance to reports.
4. Expand the CLI and experiment configuration without introducing a dashboard or physical-hardware dependency.
5. Add CI quality checks and document the remaining validation boundary.
