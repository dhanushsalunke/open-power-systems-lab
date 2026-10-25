EESchema Schematic File Version 4
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
Sheet 1 1
Title "Open Power Lab Low-Voltage Interface"
Comment1 "Reference source; verify exact MCU, ADC, connector, and protection parts"
$EndDescr
Text Notes 900 1000 0 100 ~ 20
LOW-VOLTAGE MEASUREMENT AND CONTROL INTERFACE
Text Notes 1100 1800 0 60 ~ 12
VIN_SENSE: protected divider input, range must be selected with ADC reference
Text Notes 1100 2200 0 60 ~ 12
I_SENSE: shunt/amplifier input, verify common-mode and bandwidth
Text Notes 1100 2600 0 60 ~ 12
TEMP_SENSE: NTC or analog sensor input, firmware range-check required
Text Notes 1100 3000 0 60 ~ 12
UART_TX / UART_RX / 3V3 / GND: host interface; add ESD and level compatibility review
Text Label 1200 3800 0 50 ~ 0
VIN_SENSE
Text Label 1200 4000 0 50 ~ 0
I_SENSE
Text Label 1200 4200 0 50 ~ 0
TEMP_SENSE
Text Label 1200 4400 0 50 ~ 0
UART_TX
Text Label 1200 4600 0 50 ~ 0
UART_RX
Text Label 1200 4800 0 50 ~ 0
3V3
Text Label 1200 5000 0 50 ~ 0
GND
$EndSCHEMATC
