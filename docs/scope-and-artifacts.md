# Scope and retained artifacts

This release is software-only. It does not create, validate, or recommend a fabrication-ready electronics design.

The initial repository contained a KiCad design folder. It has been removed from this project because physical design files are outside the permanent software-only scope. The remaining `firmware/` folder is a portable state-machine example only; it has no device-specific pin map, hardware connection, or build claim.

No physical measurements, ngspice runs, KiCad checks, Renode runs, firmware builds, or hardware-in-the-loop claims are included in the release evidence.
