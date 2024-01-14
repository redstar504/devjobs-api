from django.contrib.gis.geos import Point

from app.util.geocoder import coordinates_from_place_id


def km_between_points(point_a, point_b):
    return round(point_a.distance(point_b)) * 100


def km_between_place_and_point(place_id, point):
    place_coords = coordinates_from_place_id(place_id)
    place_point = Point(place_coords[0], place_coords[1])
    return km_between_points(point, place_point)
