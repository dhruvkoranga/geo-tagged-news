from geopy.geocoders import Nominatim
from functools import lru_cache

geolocator = Nominatim(user_agent="geo_tagged_news")


@lru_cache(maxsize=1000)
def resolve_location(name: str):
    location = geolocator.geocode(name)

    if not location:
        return None

    return {
        "name": name,
        "latitude": location.latitude,
        "longitude": location.longitude,
        "address": location.address
    }
