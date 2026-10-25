# Contributing

Every new model must document units, equations, assumptions, valid operating range, and limitations. Add an independent analytical test or acceptance criterion before changing a reference result.

Run `pytest -q` and `python -m open_power_lab run --config configs/baseline.yaml --output results/local` before opening a pull request. Do not commit generated local results unless they are intentionally promoted as a reference run.
