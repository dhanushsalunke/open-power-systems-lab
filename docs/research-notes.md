# Reference-project review

This project was designed after reviewing the four references named in the brief.

| Reference | Useful capability | Gap this project addresses |
|---|---|---|
| [Power Electronics Simulation Suite ngspice](https://github.com/mrdimara/Power_Electronics_Simulation_Suite_ngspice) | Organized ngspice models, examples, and learning material | This lab starts with a Python system-level API, typed configuration, fault verdicts, and reproducible reports that can later call circuit solvers |
| [Photovoltaic System Digital Twin](https://github.com/vicena-labs/photovoltaic-system-digital-twin) | Broad digital-twin workflow, validation language, and reference runs | This lab is converter/control-centric and exposes a compact plant/controller/fault/HIL contract for non-PV systems |
| [STM32 Zonal Architecture Digital Twin](https://github.com/LakshyaTaneja/STM32-Zonal-Architecture-Digital-Twin) | Embedded HIL framing, battery model, CAN-oriented controller workflow | This lab keeps simulation-only mode first-class and makes malformed-message handling and evidence boundaries explicit |
| [Renode](https://github.com/renode/renode) | Mature embedded-system emulation and peripheral simulation | Renode integration is an extension point; this repository provides the plant/protocol contract it would consume rather than pretending an MCU was emulated |

No source code was copied. These projects remain the authoritative source for their own licenses and capabilities. The research review is qualitative and should be refreshed when selecting a concrete ngspice or Renode integration.
