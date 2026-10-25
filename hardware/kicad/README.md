# Low-voltage measurement/control interface

The KiCad sources in this folder are a reference starting point for a protected low-voltage measurement interface: screw-terminal input, divider/current-sense inputs, temperature input, 3.3 V logic header, and USB/UART expansion.

The symbols and footprints are intentionally conservative placeholders until a specific MCU, ADC range, connector family, creepage requirement, and manufacturer stackup are selected. Review every pin, footprint, net class, and rating against primary datasheets before fabrication. ERC/DRC and manufacturing output were not run in this environment.
