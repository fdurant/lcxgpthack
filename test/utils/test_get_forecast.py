from utils import get_forecast
from .conftest import DUMMY_PRED_1, EXPECTED_FORECAST_1

def test_returns_as_expected():
    actual = get_forecast(prediction=DUMMY_PRED_1)

    assert actual == EXPECTED_FORECAST_1
