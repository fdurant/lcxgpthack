import pytest

from utils import get_country_code

@pytest.mark.parametrize("lat,lon, expected", [
    (50.85103, 4.2797, "be"),
    (48.8656331, 2.3212357, "fr")
])
def test_returns_expected_value(lat, lon, expected):
    actual = get_country_code(lat, lon)

    assert actual == expected
