# Open Power Systems Lab report

- Experiment: `release-baseline`
- Software version: `0.2.0`
- Status: `COMPLETE`
- Solver: `forward_euler` at `5e-05` s

## Run status

Verdict: **PASS** (simulation-only acceptance check)

## Metrics

- **steady_state_error_v**: `-0.010586294477236358`
- **peak_overshoot_v**: `1.5879709375135524`
- **rms_error_v**: `0.8081589786906774`
- **rise_time_s**: `0.00030000000000000003`
- **settling_time_s**: `0.1232`
- **max_current_a**: `2.890039819356525`
- **max_temperature_c**: `56.149697741021626`
- **efficiency_percent**: `91.61943135837554`
- **energy_balance_residual_j**: `-0.015654081612424632`
- **fault_events**: `['load_step', 'sensor_bias']`
- **warnings**: `[]`
- **verdict**: `PASS`

## Configuration

```json
{
  "simulation": {
    "duration_s": 0.25,
    "timestep_s": 5e-05,
    "seed": 7,
    "output_decimation": 1
  },
  "plant": {
    "input_voltage_v": 12.0,
    "reference_voltage_v": 5.0,
    "inductance_h": 0.00047,
    "capacitance_f": 0.0001,
    "inductor_resistance_ohm": 0.08,
    "switch_resistance_ohm": 0.06,
    "diode_drop_v": 0.55,
    "load_resistance_ohm": 5.0,
    "current_limit_a": 3.0,
    "thermal_resistance_c_per_w": 18.0,
    "conduction_mode": "dcm_approx"
  },
  "controller": {
    "kp": 0.08,
    "ki": 35.0,
    "duty_min": 0.02,
    "duty_max": 0.9
  },
  "initial_conditions": {
    "inductor_current_a": 0.0,
    "output_voltage_v": 0.0,
    "temperature_c": 25.0
  },
  "solver": {
    "method": "forward_euler",
    "max_state_abs": 1000000.0,
    "fail_on_ccm_boundary": true
  },
  "faults": [
    {
      "type": "load_step",
      "time_s": 0.12,
      "value": 2.5,
      "duration_s": null
    },
    {
      "type": "sensor_bias",
      "time_s": 0.18,
      "value": 0.03,
      "duration_s": null
    }
  ]
}
```

## Artifacts

- `signals.csv`
- `summary.json`
- `transient.png`

## Evidence boundary

This report is generated from an averaged software model. It is not a hardware safety validation, thermal qualification, EMC result, or converter certification.
