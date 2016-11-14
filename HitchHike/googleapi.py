import os
import requests

class GoogleApi:
    _geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?place_id={0}&key={1}'
    _distance_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins={0},{1}&destinations={2},{3}&key={4}'
    _api_key = 'AIzaSyCMXvF5nhmLpAYb6HcZ4YtUWDWlGcMlpE8'
    

    @classmethod
    def reverse_geo_code(cls, place_id):
        tu = (place_id, cls._api_key)
        location = requests.get(cls._geocode_url.format(*tu))
        lat = str(location.json()['results'][0]['geometry']['location']['lat'])
        lng = str(location.json()['results'][0]['geometry']['location']['lng'])

        return [lat, lng]

    @classmethod
    def distance(cls, origin, destination):
        origin_cod = cls.reverse_geo_code(origin)
        destination_cod = cls.reverse_geo_code(destination)
        origin_lat = origin_cod[0]
        origin_lng = origin_cod[1]
        destination_lat = destination_cod[0]
        destination_lng = destination_cod[1]

        distance_data = requests.get(cls._distance_url.format(origin_lat, origin_lng, destination_lat, destination_lng, cls._api_key))
        print distance_data.json()
        dist = distance_data.json()['rows'][0]['elements'][0]['distance']['value']

        return dist