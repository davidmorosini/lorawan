import pytest

from py2Solve.decoder import Decoder

MOCKED_RESPONSE = {
    "json2sense": {
        "drainage_PH": 7.888,
        "drainage_PH_SD": 0.0,
        "drainage_Turbidity": 1474.0,
        "drainage_Turbidity_SD": 0.0,
        "drainage_Conductivity": 493.0,
        "drainage_Conductivity_SD": 0.0,
        "drainage_Temp": 29.89,
        "drainage_Temp_SD": 0.0,
    }
}

MOCKED_RESPONSE_2 = {
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
}

MOCKED_RESPONSE_3 = {"json2sense": {"water_level": 390.708, "BatteryMon_IC": 10.979}}


@pytest.mark.parametrize(
    ("payload", "offset", "fport", "expected"),
    [
        (
            "gB1A/Gp/gCQAAAAAgB5EuEAAgCUAAAAAgB9D9oAAgCYAAAAAgCNB7x64gCcAAAAA",
            0,
            None,
            MOCKED_RESPONSE,
        ),
        (
            "gB1A9P30gCQAAAAAgB5DxIAAgCUAAAAAgB9C1AAAgCYAAAAAgCNCA6PXgCcAAAAA",
            0,
            None,
            MOCKED_RESPONSE_2,
        ),
        ("gC5Dw1qggDBBL6n8", 0, None, MOCKED_RESPONSE_3),
    ],
)
def test_payload_decode(payload, offset, fport, expected):
    assert expected == Decoder.decode(payload=payload, offset=offset, fport=fport)
