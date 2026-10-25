# Changelog

## 0.3.0 - 2026-10-25

- Removed all KiCad schematics, PCB layouts, and KiCad-only documentation from the repository.
- Established the software-only project boundary for future contributions.

## 0.2.0 - 2026-10-25

- Added repository audit and explicit software-only scope boundary.
- Added strict CCM validity checks and a declared startup-compatible DCM approximation.
- Added timestep robustness, fault-duration, transient metrics, energy residual, efficiency, and baseline-vs-fault comparison.
- Added software-only Thevenin battery model with OCV interpolation, SOC accounting, efficiency, and operating limits.
- Added `models`, `validate`, `sweep`, `compare`, and `verify` CLI commands.
- Added Ruff, mypy, compile, packaging, and reproducible-workflow CI checks.

## 0.1.0 - 2026-10-25

- Added averaged buck plant, PI controller, fault injection, diagnostics, reporting, CLI, protocol validation, tests, and a portable firmware state-machine example.
