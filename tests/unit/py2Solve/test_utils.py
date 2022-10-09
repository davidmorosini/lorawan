import math

import pytest

from py2Solve.tools import (
    _2pow,
    base64_string_to_byte_string,
    base64_to_hex_buffer,
    float_from_byte_array,
    get_field_name_by_id,
    hex_to_dec,
    is_hex,
    packet_decode,
)


@pytest.mark.parametrize(
    ("exponent", "expected"),
    [(0, 1), (3, 8), (-3, 0.125)],
)
def test_utils_2pow(exponent, expected):
    assert expected == _2pow(exponent)


@pytest.mark.parametrize(
    ("string", "expected"),
    [("02BA", True), ("02BG", False)],
)
def test_utils_is_hex(string, expected):
    assert expected == is_hex(string)


@pytest.mark.parametrize(
    ("hex_string", "expected"),
    [("abcd", 43981), ("ABCD", 43981)],
)
def test_utils_hex_to_dec(hex_string, expected):
    assert expected == hex_to_dec(hex_string)


@pytest.mark.parametrize(
    ("base64_str", "expected"),
    [
        ("dGVzdGU=", ["0x74", "0x65", "0x73", "0x74", "0x65"]),
    ],
)
def test_utils_base64_to_hex_buffer(base64_str, expected):
    assert expected == base64_to_hex_buffer(base64_str)


@pytest.mark.parametrize(
    ("base64_str", "expected"),
    [
        ("dGVzdGU=", "7465737465"),
    ],
)
def test_utils_base64_string_to_byte_string(base64_str, expected):
    assert expected == base64_string_to_byte_string(base64_str)


@pytest.mark.parametrize(
    ("field_mapping", "id", "expected"),
    [
        ({"a": [5, 1, None, "uint"]}, 5, "a"),
    ],
)
def test_utils_get_field_name_by_id(field_mapping, id, expected):
    assert expected == get_field_name_by_id(field_mapping, id)


@pytest.mark.parametrize(
    ("field_mapping", "id", "exception", "error_message"),
    [
        ({"a": [5, 1, None, "uint"]}, 4, Exception, "ID '4' not found"),
    ],
)
def test_utils_get_field_name_by_id_error(field_mapping, id, exception, error_message):
    with pytest.raises(exception) as e:
        get_field_name_by_id(field_mapping, id)

    assert error_message == str(e.value)


@pytest.mark.parametrize(
    ("byte_array", "expected"),
    [([64, 244, 253, 244], 7.656000137329102)],
)
def test_utils_float_from_byte_array(byte_array, expected):
    assert expected == float_from_byte_array(byte_array)


@pytest.mark.parametrize(
    ("byte_array", "expected"),
    [([64, 244, 253, 244], False), ([255, 128, 0, 0], False), ([127, 200, 100, 181], True)],
)
def test_utils_float_from_byte_array_is_nan(byte_array, expected):
    value = float_from_byte_array(byte_array)
    assert expected == math.isnan(value)


@pytest.mark.parametrize(
    ("byte_array", "expected"),
    [([64, 244, 253, 244], False), ([127, 200, 100, 181], False), ([255, 128, 0, 0], True)],
)
def test_utils_float_from_byte_array_is_inf(byte_array, expected):
    value = float_from_byte_array(byte_array)
    assert expected == math.isinf(value)


@pytest.mark.parametrize(
    ("payload", "offset", "fport", "exception", "error_message"),
    [
        ("dGVzdGU=", "0", None, Exception, "Offset format must be a positive integer number"),
        ("dGVzdGU=", 900, None, Exception, "Wrong offset value"),
        ("dGVzdGU=", -1, None, Exception, "Wrong offset value"),
    ],
)
def test_utils_packet_decode_raises(payload, offset, fport, exception, error_message):
    with pytest.raises(exception) as e:
        packet_decode(payload, offset, fport)

    assert error_message == str(e.value)


@pytest.mark.parametrize(
    ("payload", "offset", "fport", "expected"),
    [
        (
            "gB1A9P30gCQAAAAAgB5DxIAAgCUAAAAAgB9C1AAAgCYAAAAAgCNCA6PXgCcAAAAA",
            0,
            None,
            {
                "json2sense": {
                    "drainage_PH": 7.656,
                    "drainage_PH_SD": 0.0,
                    "drainage_Turbidity": 393.0,
                    "drainage_Turbidity_SD": 0.0,
                    "drainage_Conductivity": 106.0,
                    "drainage_Conductivity_SD": 0.0,
                    "drainage_Temp": 32.91,
                    "drainage_Temp_SD": 0.0,
                }
            },
        )
    ],
)
def test_utils_packet_decode(payload, offset, fport, expected):
    assert expected == packet_decode(payload, offset, fport)
