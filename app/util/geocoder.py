import googlemaps

def coordinates_from_place_id(place_id):
    gmaps = googlemaps.Client(key='AIzaSyAVrYTZpKroI1W7ZOsxKyRiCoUR6DGHfXU')
    geocode_result = gmaps.geocode(place_id='ChIJufI-cg9EXj4RCBGXQZMuzMc')