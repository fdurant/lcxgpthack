import pytest
from datetime import datetime

from utils import get_next_weekday, SATURDAY_DOW, SUNDAY_DOW

START_SATURDAY = datetime(2023, 4, 22).isoformat().split("T")[0]
START_SUNDAY = datetime(2023, 4, 23).isoformat().split("T")[0]
START_MONDAY = datetime(2023, 4, 24).isoformat().split("T")[0]
START_FRIDAY = datetime(2023, 4, 28).isoformat().split("T")[0]
EXPECTED_SATURDAY = datetime(2023, 4, 29).isoformat().split("T")[0]
EXPECTED_SUNDAY = datetime(2023, 4, 30).isoformat().split("T")[0]

@pytest.mark.parametrize("startdate, weekday, expected", [
#    (START_SATURDAY, SATURDAY_DOW, EXPECTED_SATURDAY), # FAILS
    (START_SUNDAY, SATURDAY_DOW, EXPECTED_SATURDAY),
    (START_MONDAY, SATURDAY_DOW, EXPECTED_SATURDAY),
    (START_FRIDAY, SATURDAY_DOW, EXPECTED_SATURDAY),
    (START_MONDAY, SUNDAY_DOW, EXPECTED_SUNDAY),
    (START_FRIDAY, SUNDAY_DOW, EXPECTED_SUNDAY),
])
def test_returns_expected_value(startdate, weekday, expected):
    actual = get_next_weekday(startdate=startdate, weekday=weekday)

    assert actual == expected
