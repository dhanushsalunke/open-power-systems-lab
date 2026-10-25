import argparse
from .config import load_config
from .reporting import write_report
from .simulation import run
from .analysis import stability_margin

def main() -> int:
    parser = argparse.ArgumentParser(prog="opl", description="Open Power Systems Lab")
    sub = parser.add_subparsers(dest="command", required=True)
    run_parser = sub.add_parser("run", help="run a configured simulation")
    run_parser.add_argument("--config", required=True)
    run_parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.command == "run":
        cfg = load_config(args.config)
        result = run(cfg)
        summary = write_report(result, args.output, cfg.plant.reference_voltage_v, cfg.simulation.timestep_s, cfg.plant.current_limit_a)
        margins = stability_margin(cfg)
        print(f"{summary['verdict']}: {args.output}")
        print(f"steady-state error={summary['steady_state_error_v']:.4f} V, peak current={summary['max_current_a']:.4f} A")
        print(f"gain crossover={margins['gain_crossover_hz']} Hz, phase margin={margins['phase_margin_deg']} deg")
    return 0

if __name__ == "__main__": raise SystemExit(main())
