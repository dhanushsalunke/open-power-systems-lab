from pathlib import Path
import csv, json
import numpy as np
from .diagnostics import evaluate
from .simulation import SimulationResult

def write_report(result: SimulationResult, output: str | Path, reference_v: float, timestep_s: float, current_limit_a: float) -> dict:
    folder = Path(output); folder.mkdir(parents=True, exist_ok=True)
    summary = evaluate(result.data, reference_v, timestep_s, current_limit_a)
    result.summary = summary
    keys = list(result.data)
    with (folder / "signals.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f); writer.writerow(keys)
        for row in zip(*(result.data[k] for k in keys)): writer.writerow(row)
    (folder / "summary.json").write_text(json.dumps(summary.to_dict(), indent=2), encoding="utf-8")
    report = "# Open Power Systems Lab report\n\n"
    report += "## Run status\n\n"
    report += f"Verdict: **{summary.verdict}** (simulation-only acceptance check)\n\n"
    report += "## Metrics\n\n"
    for key, value in summary.to_dict().items(): report += f"- **{key}**: `{value}`\n"
    report += "\n## Evidence boundary\n\nThis report is generated from an averaged software model. It is not a hardware safety validation, thermal qualification, EMC result, or converter certification.\n"
    (folder / "report.md").write_text(report, encoding="utf-8")
    try:
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(3, 1, figsize=(9, 8), sharex=True)
        t = result.data["time_s"]
        axes[0].plot(t, result.data["output_voltage_v"], label="Vout"); axes[0].axhline(reference_v, color="k", ls="--", label="reference"); axes[0].set_ylabel("V"); axes[0].legend()
        axes[1].plot(t, result.data["inductor_current_a"], label="inductor current"); axes[1].set_ylabel("A"); axes[1].legend()
        axes[2].plot(t, result.data["duty"], label="duty"); axes[2].set_ylabel("ratio"); axes[2].set_xlabel("time (s)"); axes[2].legend()
        fig.tight_layout(); fig.savefig(folder / "transient.png", dpi=140); plt.close(fig)
    except ImportError:
        pass
    return summary.to_dict()
