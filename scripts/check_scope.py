"""Fail if forbidden physical-design artifacts are added to this repository."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_EXTENSIONS = {
    ".sch",
    ".kicad_sch",
    ".kicad_pcb",
    ".kicad_pro",
    ".kicad_prl",
    ".kicad_wks",
    ".kicad_mod",
    ".kicad_sym",
    ".net",
}
FORBIDDEN_DIRECTORIES = {"kicad", "kicad_pro", "kicad_pcb"}


def main() -> int:
    violations: list[str] = []
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.is_dir() and (
            path.name.lower() in FORBIDDEN_DIRECTORIES
            or path.name.lower().endswith(".pretty")
        ):
            violations.append(str(path.relative_to(ROOT)))
        elif path.is_file() and path.suffix.lower() in FORBIDDEN_EXTENSIONS:
            violations.append(str(path.relative_to(ROOT)))
    if violations:
        print("Forbidden physical-design artifacts found:")
        print("\n".join(sorted(violations)))
        return 1
    print("Scope check passed: no KiCad or PCB design artifacts found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
