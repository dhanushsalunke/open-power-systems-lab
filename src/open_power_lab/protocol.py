"""Minimal JSON-lines protocol for a future serial or TCP adapter."""
import json
from dataclasses import dataclass

@dataclass(frozen=True)
class Measurement:
    timestamp_us: int
    voltage_v: float
    current_a: float
    temperature_c: float
    status: str = "OK"

def encode_measurement(m: Measurement) -> str:
    if m.timestamp_us < 0 or not all(map(lambda x: x == x, (m.voltage_v, m.current_a, m.temperature_c))):
        raise ValueError("invalid measurement")
    return json.dumps({"type": "measurement", "timestamp_us": m.timestamp_us, "voltage_v": m.voltage_v, "current_a": m.current_a, "temperature_c": m.temperature_c, "status": m.status}, separators=(",", ":"))

def decode_message(line: str) -> dict:
    try: message = json.loads(line)
    except json.JSONDecodeError as exc: raise ValueError("malformed JSON message") from exc
    if not isinstance(message, dict) or message.get("type") not in {"measurement", "command", "heartbeat", "fault"}:
        raise ValueError("unsupported message type")
    if "timestamp_us" not in message or not isinstance(message["timestamp_us"], int):
        raise ValueError("timestamp_us integer is required")
    return message
