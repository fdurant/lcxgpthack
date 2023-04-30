from typing import Optional, Text, List, Dict, Tuple
import geocoder
from geopy.geocoders import Nominatim
from citipy import citipy
from citipy.citipy import WORLD_CITIES_DICT

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