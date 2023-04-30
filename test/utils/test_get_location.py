import pytest

from utils import get_location

@pytest.mark.parametrize("place_name, expected", [
    ("Brussels,BE", [50.8465573, 4.351697]),
    ("New York City, USA", [40.7127281, -74.0060152])
])
def test_returns_expected_value(place_name, expected):
    actual = get_location(place_name=place_name)

    assert actual == expected
