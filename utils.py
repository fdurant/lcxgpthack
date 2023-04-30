from typing import Optional, Text, List, Dict
import geocoder
from geopy.geocoders import Nominatim
from citipy import citipy
from citipy.citipy import WORLD_CITIES_DICT

def get_location() -> List[float]:
    g = geocoder.ip('me')
    return g.latlng

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