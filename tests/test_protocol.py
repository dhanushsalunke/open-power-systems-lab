import pytest
from open_power_lab.protocol import Measurement, encode_measurement, decode_message


def test_protocol_round_trip():
    message = decode_message(encode_measurement(Measurement(12, 5.0, 1.2, 31.0)))
    assert message["type"] == "measurement"
    assert message["voltage_v"] == 5.0


def test_protocol_rejects_malformed_message():
    with pytest.raises(ValueError):
        decode_message("not-json")
    with pytest.raises(ValueError):
        decode_message('{"type":"measurement"}')
