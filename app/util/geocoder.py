import googlemaps

gmaps = googlemaps.Client(key='AIzaSyAVrYTZpKroI1W7ZOsxKyRiCoUR6DGHfXU')


def coordinates_from_place_id(place_id):
    geocode_result = gmaps.geocode(place_id=place_id)
    loc = geocode_result[0]["geometry"]["location"]
    return loc["lat"], loc["lng"]


def coordinates_from_city_country(city, country):
    res = gmaps.geocode(f'{city}, {country}')
    loc = res[0]["geometry"]["location"]
    return loc["lat"], loc["lng"]


print(coordinates_from_place_id('ChIJufI-cg9EXj4RCBGXQZMuzMc'))
