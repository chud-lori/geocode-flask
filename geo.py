from config import Config
import requests

class Geo(object):
    
    def is_inside(self, origin, destination) -> bool:
        """
            this method will check if destination inside the origin by comparing the destination latitude longitude is in origin's bounds
            return:
                it will return boolean True or False
        """
        origin: dict = self.get_location(origin)[0]
        origin_bounds = origin['results'][0]['geometry']['bounds']
        origin = {
            "bound_north_lat": origin_bounds['northeast']['lat'],
            "bound_north_lng": origin_bounds['northeast']['lng'],
            "bound_south_lat": origin_bounds['southwest']['lat'],
            "bound_south_lng": origin_bounds['southwest']['lng']
            }

        destination_lat, destination_lng = self.get_location(destination)[-2:]

        if float(destination_lat) > float(origin["bound_south_lat"]) and float(destination_lng) > float(origin["bound_south_lng"]) and float(destination_lat) < float(origin["bound_north_lat"]) and float(destination_lng) < float(origin["bound_north_lng"]):
            return True
        return False
    
    @staticmethod
    def get_distance(origin_place_id: str, destination_place_id: str) -> tuple:
        """
        parameter require the place_id of origin and destination location
        return:
            distance will return in meters, duration will return in seconds
            (distance: int, duration: int)
        """

        distance: dict = requests.get(f'https://maps.googleapis.com/maps/api/distancematrix/json?origins=place_id:{origin_place_id}&destinations=place_id:{destination_place_id}&key={Config.GEO_KEY}').json()

        if distance['rows'][0]['elements'][0]['status'] != "OK":
            return ('Distance too far or not available', False)

        distance_meters: int = distance['rows'][0]['elements'][0]['distance']['value']
        duration_seconds: int = distance['rows'][0]['elements'][0]['duration']['value']

        return (distance_meters, duration_seconds)

    @staticmethod
    def get_location(location: str) -> tuple:
        """
        parameters:
            location: string = require a location name in string
        return:
            if location found it will return in tuple format:
                (location_json, place_id, lat, lng)
            if not found it will return False in boolean
        """
        location_json: dict = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={Config.GEO_KEY}').json()

        if location_json["status"] != "OK":
            return ('Not found', False)

        place_id: str = location_json['results'][0]['place_id']
        lat: str = location_json['results'][0]['geometry']['location']['lat']
        lng: str = location_json['results'][0]['geometry']['location']['lng']

        return (location_json, place_id, lat, lng)
