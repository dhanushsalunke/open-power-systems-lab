import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path
from . import __version__
from .analysis import compare_scenarios, parameter_sweep, stability_margin
from .config import load_config
from .reporting import write_report
from .simulation import run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="opl", description="Open Power Systems Lab")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("models", help="list supported software models")
    validate = sub.add_parser("validate", help="validate a YAML configuration")
    validate.add_argument("--config", required=True)
    run_parser = sub.add_parser("run", help="run a configured simulation")
    run_parser.add_argument("--config", required=True)
    run_parser.add_argument("--output", required=True)
    sweep = sub.add_parser("sweep", help="run a deterministic plant-parameter sweep")
    sweep.add_argument("--config", required=True)
    sweep.add_argument("--parameter", required=True)
    sweep.add_argument("--values", required=True, help="comma-separated numeric values")
    sweep.add_argument("--output", required=True)
    compare = sub.add_parser(
        "compare", help="compare configured faults with a no-fault baseline"
    )
    compare.add_argument("--config", required=True)
    compare.add_argument("--output", required=True)
    sub.add_parser("verify", help="run the repository verification suite")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "models":
        print(
            "buck-averaged-ccm: averaged continuous-conduction buck converter (strict zero-current boundary)"
        )
        print(
            "buck-averaged-dcm_approx: startup-compatible zero-current clipping approximation"
        )
        print(
            "battery-thevenin: static OCV-SOC and internal-resistance energy-storage model"
        )
        print(
            "pi-voltage-controller: saturated PI controller with conditional anti-windup"
        )
        return 0
    if args.command == "validate":
        cfg = load_config(args.config)
        print(
            f"valid configuration: {args.config} ({cfg.plant.conduction_mode}, {cfg.solver.method})"
        )
        return 0
    if args.command == "run":
        cfg = load_config(args.config)
        result = run(cfg)
        summary = write_report(result, args.output, cfg)
        margins = stability_margin(cfg)
        print(f"{summary['verdict']}: {args.output}")
        print(
            f"steady-state error={summary['steady_state_error_v']:.4f} V, peak current={summary['max_current_a']:.4f} A"
        )
        print(
            f"gain crossover={margins['gain_crossover_hz']} Hz, phase margin={margins['phase_margin_deg']} deg"
        )
        return 0
    if args.command == "sweep":
        cfg = load_config(args.config)
        rows = parameter_sweep(
            cfg, args.parameter, [float(value) for value in args.values.split(",")]
        )
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"wrote {len(rows)} sweep points to {output}")
        return 0
    if args.command == "verify":
        return subprocess.run(
            [sys.executable, "-m", "pytest", "-q"], check=False
        ).returncode
    if args.command == "compare":
        cfg = load_config(args.config)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(compare_scenarios(cfg), indent=2), encoding="utf-8"
        )
        print(f"wrote baseline-vs-fault comparison to {output}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
