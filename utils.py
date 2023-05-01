from typing import Optional, Text, List, Dict, Tuple, Any
import geocoder
from geopy.geocoders import Nominatim
from citipy import citipy
from citipy.citipy import WORLD_CITIES_DICT
from datetime import datetime, timedelta
from dictor import dictor

SATURDAY_DOW = 5
SUNDAY_DOW = 6

def get_location(place_name: Optional[Text] = None) -> List[float]:
    latlon_as_list = [40.7127281, -74.0060152]  # NYC
    loc = None
    if place_name:
        try:
            geolocator = Nominatim(timeout=10, user_agent="Krukarius")
            loc = geolocator.geocode(place_name)
        except Exception:
            pass
        if loc:
            latlon : Tuple = loc[1]
            latlon_as_list = [latlon[0], latlon[1]]
    else:
        try:
            g = geocoder.ip('me')
            latlon_as_list = g.latlng
        except Exception:
            pass
    return latlon_as_list

def get_country_code(lat: float, lon: float) -> Optional[Text]:
    result = "us"
    location = None
    try:
        geolocator = Nominatim(user_agent="my_app")
        location = geolocator.reverse((lat, lon), exactly_one=True)
    except Exception:
        pass
    if location:
        try:
            return location.raw['address']['country_code']
        except (AttributeError, KeyError):
            pass
    return result

def get_all_cities_by_country() -> Dict[Text, citipy.City]:
    d = {}
    for _, city in WORLD_CITIES_DICT.items():
        country_code = city.country_code
        if country_code in d:
            d[country_code].append(city)
        else:
            d[country_code] = [city]
    return d

CITIES_BY_COUNTRY = get_all_cities_by_country()

def get_cities(country_code: str) -> List[Text]:
    cities = CITIES_BY_COUNTRY.get(country_code)
    return [city.city_name for city in cities]

# From https://stackoverflow.com/questions/16769902/finding-the-date-of-the-next-saturday
def get_next_weekday(startdate: datetime, weekday) -> datetime:
    """
    @startdate: given datetime
    @weekday: week day as a integer, between 0 (Monday) to 6 (Sunday)
    """
    days_per_week = 7
    offset = timedelta((days_per_week + weekday - startdate.weekday()) % days_per_week)
    next_weekday_midnight = (startdate + offset).strftime('%Y-%m-%d')
    return datetime.fromisoformat(next_weekday_midnight)


def select_weather_prediction_by_date(predictions: List[Dict], dt_query: datetime) -> Optional[Dict[Text, Text]]:
    # Loop over list to find the prediction for dt_query (exact match only!)
    # Returns a dict like {
    #    "dt":1683111600,
    #    "temp":{
    #        "day":12.56,
    #        "min":2.55,
    #        "max":15.12,
    #        "night":9.96,
    #        "eve":14.12,
    #        "morn":2.72,
    #    },
    #   "weather": [
    #        {
    #            "id":804,
    #            "main":"Clouds",
    #            "description":"overcast clouds",
    #            "icon":"04n"}
    #    ]
    #}
    # or None if nothing is found

    dt_key = "dt"
    result = {}
    print(f"dt_query is ", dt_query)
    for pred in predictions:
        print("prediction is", pred)
        if dt_key in pred:
            dt = datetime.fromtimestamp(pred.get(dt_key))
            print("reference dt is ", dt)
            if dt_query.year == dt.year and dt_query.month == dt.month and dt_query.day == dt.day:
                try:
                    result = pred
                except (KeyError, IndexError, AttributeError):
                    pass
    return result

def get_forecast(prediction: Dict[Text, Any]) -> Text:
    # @prediction: a dict like {
    #    "dt":1683111600,
    #    "temp":{
    #        "day":12.56,
    #        "min":2.55,
    #        "max":15.12,
    #        "night":9.96,
    #        "eve":14.12,
    #        "morn":2.72,
    #    },
    #   "weather": [
    #        {
    #            "id":804,
    #            "main":"Clouds",
    #            "description":"overcast clouds",
    #            "icon":"04n"}
    #    ]
    #}
    # Returns a written forecast
    weather_forecast = dictor(prediction, "weather.0.description")
    temp_outlook = "temperature up to " + str(int(dictor(prediction, "temp.max"))) + " °C"
    forecast = ""
    if weather_forecast:
        forecast += f"{weather_forecast}. "
    if temp_outlook:
        forecast += f"{temp_outlook}."
    return forecast
