from config import Config
import requests
import logging
from datetime import date

class Geo(object):
    def __init__(self) -> None:
        self.log_name: str = f'{str(date.today())}.log'
        
    def check_distance(self, origin, destination) -> bool:
        matr = requests.get(f'https://maps.googleapis.com/maps/api/distancematrix/json?origins=place_id:{origin}&destinations=place_id:{destination}&key={Config.GEO_KEY}')
        if value < 1:
            # No log
            return False
        # Write log
        return True
    
    @staticmethod
    def get_distance(origin_place_id: str, destination_place_id: str) -> tuple:
        """
        parameter require the place_id of origin and destination location
        return:
            distance will return in meters, duration will return in seconds
            (distance: int, duration: int)
        """

        distance: dict = requests.get(f'https://maps.googleapis.com/maps/api/distancematrix/json?origins=place_id:{origin_place_id}&destinations=place_id:{destination_place_id}&key={Config.GEO_KEY}').json()
        if distance.get('rows')[0].get('elements')[0].get('status') != "OK":
            return ('Distance too far or not available', False)

        distance_meters: int = distance.get('rows')[0].get('elements')[0].get('distance').get('value')
        duration_seconds: int = distance.get('rows')[0].get('elements')[0].get('duration').get('value')

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

        if location_json.get("status") != "OK":
            return ('Not found', False)

        place_id: str = location_json.get('results')[0].get('place_id')
        lat: str = location_json.get('results')[0].get('geometry').get('location').get('lat')
        lng: str = location_json.get('results')[0].get('geometry').get('location').get('lng')

        return (location_json, place_id, lat, lng)
