from typing import Optional, Text, List, Dict, Tuple
import geocoder
from geopy.geocoders import Nominatim
from citipy import citipy
from citipy.citipy import WORLD_CITIES_DICT
from datetime import datetime, timedelta

SATURDAY_DOW = 5
SUNDAY_DOW = 6

def get_location(place_name: Optional[Text] = None) -> List[float]:
    latlon_as_list = []
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
        g = geocoder.ip('me')
        latlon_as_list = g.latlng
    return latlon_as_list

def get_country_code(lat: float, lon: float) -> Optional[Text]:
    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    result = None
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
def get_next_weekday(startdate, weekday):
    """
    @startdate: given date, in format '2013-05-25'
    @weekday: week day as a integer, between 0 (Monday) to 6 (Sunday)
    """
    d = datetime.strptime(startdate, '%Y-%m-%d')
    t = timedelta((7 + weekday - d.weekday()) % 7)
    return (d + t).strftime('%Y-%m-%d')


def find_weather_prediction_by_date(predictions: List[Dict], dt: datetime.time) -> Optional[Dict[Text, Text]]:
    # Loop over list to find the prediction for a day at noon
    # Returns a dict like {
    #        "id": 500,
    #        "main": "Rain",
    #        "description": "light rain",
    #        "icon": "10n"
    #    }
    # or None
    return {
            "id": 500,
            "main": "Rain",
            "description": "light rain",
            "icon": "10n"
        }
