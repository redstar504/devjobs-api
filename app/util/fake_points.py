from django.contrib.gis.geos import Point


def coords_of_moscow():
    return 37.6173, 55.755826


def point_of_moscow():
    coords = coords_of_moscow()
    return Point(coords[0], coords[1])


def place_id_of_moscow():
    return "ChIJybDUc_xKtUYRTM9XV8zWRD0"


def coords_of_munich():
    return 11.5819806, 48.1351253


def point_of_munich():
    coords = coords_of_munich()
    return Point(coords[0], coords[1])


def place_id_of_munich():
    return "ChIJ2V-Mo_l1nkcRfZixfUq4DAE"
