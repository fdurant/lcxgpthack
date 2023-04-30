import pytest

from utils import get_cities

@pytest.mark.parametrize("country, expected_first_3", [
    ("be", ['aalst', 'aalter', 'aarschot']),
    ("fr", ['abbeville', 'ablon-sur-seine', 'acheres'])
])
def test_returns_expected_value(country, expected_first_3):
    actual = get_cities(country)

    assert actual[0:3] == expected_first_3
