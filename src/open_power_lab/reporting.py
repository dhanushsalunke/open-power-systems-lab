from pathlib import Path
import csv
import json
from dataclasses import asdict
from .diagnostics import evaluate
from .simulation import SimulationResult
from . import __version__
from .config import SystemConfig


def write_report(
    result: SimulationResult, output: str | Path, config: SystemConfig
) -> dict:
    folder = Path(output)
    folder.mkdir(parents=True, exist_ok=True)
    summary = evaluate(
        result.data,
        config.plant.reference_voltage_v,
        config.simulation.timestep_s,
        config.plant.current_limit_a,
        config.plant.inductance_h,
        config.plant.capacitance_f,
    )
    result.summary = summary
    keys = list(result.data)
    with (folder / "signals.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for row in zip(*(result.data[k] for k in keys)):
            writer.writerow(row)
    payload = {
        "experiment_id": folder.name,
        "software_version": __version__,
        "status": result.status,
        "summary": summary.to_dict(),
        "configuration": asdict(config),
        "warnings": result.warnings or [],
        "artifacts": ["signals.csv", "summary.json", "report.md", "transient.png"],
    }
    (folder / "summary.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    report = "# Open Power Systems Lab report\n\n"
    report += f"- Experiment: `{folder.name}`\n- Software version: `{__version__}`\n- Status: `{result.status}`\n- Solver: `{config.solver.method}` at `{config.simulation.timestep_s}` s\n\n"
    report += "## Run status\n\n"
    report += f"Verdict: **{summary.verdict}** (simulation-only acceptance check)\n\n"
    report += "## Metrics\n\n"
    for key, value in summary.to_dict().items():
        report += f"- **{key}**: `{value}`\n"
    report += (
        "\n## Configuration\n\n```json\n"
        + json.dumps(asdict(config), indent=2)
        + "\n```\n"
    )
    report += "\n## Artifacts\n\n- `signals.csv`\n- `summary.json`\n- `transient.png`\n"
    report += "\n## Evidence boundary\n\nThis report is generated from an averaged software model. It is not a hardware safety validation, thermal qualification, EMC result, or converter certification.\n"
    (folder / "report.md").write_text(report, encoding="utf-8")
    try:
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(3, 1, figsize=(9, 8), sharex=True)
        t = result.data["time_s"]
        axes[0].plot(t, result.data["output_voltage_v"], label="Vout")
        axes[0].axhline(
            config.plant.reference_voltage_v, color="k", ls="--", label="reference"
        )
        axes[0].set_ylabel("V")
        axes[0].legend()
        axes[1].plot(t, result.data["inductor_current_a"], label="inductor current")
        axes[1].set_ylabel("A")
        axes[1].legend()
        axes[2].plot(t, result.data["duty"], label="duty")
        axes[2].set_ylabel("ratio")
        axes[2].set_xlabel("time (s)")
        axes[2].legend()
        fig.tight_layout()
        fig.savefig(folder / "transient.png", dpi=140)
        plt.close(fig)
    except ImportError:
        pass
    return summary.to_dict()
