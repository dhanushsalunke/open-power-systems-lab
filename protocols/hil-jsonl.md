# HIL JSON-lines protocol

Each line is one UTF-8 JSON object. Every message has an integer `timestamp_us` from the sender's monotonic clock and a `type`.

Measurement: `{ "type": "measurement", "timestamp_us": 123, "voltage_v": 5.0, "current_a": 1.2, "temperature_c": 30.0, "status": "OK" }`

Command: `{ "type": "command", "timestamp_us": 123, "duty": 0.42, "enable": true }`

The host must reject malformed JSON, unknown message types, missing timestamps, NaN/Inf numeric payloads, and samples older than the configured timeout. A production adapter must add framing, serial error handling, sequence numbers, and a watchdog-controlled safe output state. This repository only implements offline validation; it does not claim a tested serial transport.
