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


def coords_of_vancouver():
    return -123.1207375, 49.2827291


def point_of_vancouver():
    coords = coords_of_vancouver()
    return Point(coords[0], coords[1])


def place_id_of_vancouver():
    return "ChIJs0-pQ_FzhlQRi_OBm-qWkbs"


def coords_of_kamloops():
    return -120.3272674, 50.674522


def point_of_kamloops():
    coords = coords_of_kamloops()
    return Point(coords[0], coords[1])


def place_id_of_kamloops():
    return "ChIJMTsNPdMsflMR50VpmqqWPtI"


def coords_of_calgary():
    return -114.0718831, 51.04473309999999


def point_of_calgary():
    coords = coords_of_calgary()
    return Point(coords[0], coords[1])


def place_id_of_calgary():
    return "ChIJ1T-EnwNwcVMROrZStrE7bSY"
