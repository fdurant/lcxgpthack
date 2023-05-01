import pytest
from datetime import datetime

from utils import select_weather_prediction_by_date
from .conftest import DUMMY_PRED_1, DUMMY_PRED_2, DUMMY_PRED_3

PREDICTIONS = [DUMMY_PRED_1, DUMMY_PRED_2, DUMMY_PRED_3]

@pytest.mark.parametrize("dt_query, expected", [
    (datetime(2023, 5, 1, 11), DUMMY_PRED_1),
    (datetime(2023, 5, 2, 11), DUMMY_PRED_2),
    (datetime(2023, 5, 3, 11), DUMMY_PRED_3)])
def test_returns_expected_value(dt_query, expected):
    actual = select_weather_prediction_by_date(predictions=PREDICTIONS, dt_query=dt_query)

    assert actual == expected
