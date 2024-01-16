import googlemaps
from django.conf import settings

from app.logger import logger
from app.util.fake_points import coords_of_moscow, coords_of_munich

gmaps = googlemaps.Client(settings.GMAPS_API_KEY)

# whether to return coordinates of moscow for place_id and coords of munich for city,country lookup
use_mocks = settings.USE_GMAPS_MOCKS


def coordinates_from_place_id(place_id):
    if use_mocks:
        logger.debug("[GeoMocks] providing coordinates of moscow.")
        return coords_of_moscow()
    else:
        geocode_result = gmaps.geocode(place_id=place_id)
        loc = geocode_result[0]["geometry"]["location"]
        return loc["lng"], loc["lat"]


def coordinates_from_city_country(city, country):
    if use_mocks:
        logger.debug("[GeoMocks] providing coordinates of munich.")
        return coords_of_munich()
    else:
        res = gmaps.geocode(f'{city}, {country}')
        loc = res[0]["geometry"]["location"]
        return loc["lng"], loc["lat"]
