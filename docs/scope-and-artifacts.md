# Scope and retained artifacts

This release is software-only. It does not create, validate, or recommend a fabrication-ready electronics design.

The initial repository contained `hardware/kicad/` and `firmware/`. They are retained to avoid silently deleting user work, but they are legacy reference artifacts and are not imported by the simulation package, CI, reports, or verification suite. Their symbols, footprints, pin assumptions, and state-machine behavior are not verified here. Future hardware work should be performed in a separately reviewed project with authoritative datasheets and actual ERC/DRC/build evidence.

No physical measurements, ngspice runs, KiCad checks, Renode runs, firmware builds, or hardware-in-the-loop claims are included in the release evidence.
