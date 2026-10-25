# Firmware extension point

The intended target is an STM32 or ESP32 low-voltage measurement/control interface. The host-side protocol is documented in `protocols/hil-jsonl.md`.

Required firmware states:

`BOOT -> SELF_TEST -> IDLE -> ARMED -> CONTROLLED -> FAULT`

The watchdog must force outputs to a safe disabled state on timeout, invalid ADC readings, over-temperature, over-current, or host communication loss. No device-specific pin map or part number is asserted yet; those must be selected from a reviewed schematic and datasheet before a hardware release.
