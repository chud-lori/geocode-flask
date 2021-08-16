from flask import (Blueprint, jsonify, redirect, request)
from flask.templating import render_template
from geo import Geo
from datetime import date, datetime

geo_bp = Blueprint('geo_bp', __name__)

# initiate object of Geo class with value of origin location
origin: str = 'Moscow Ring Road '
geo = Geo(origin)

@geo_bp.route('/')
def index() -> dict:
    """
        The main function to handle base route (/)
        It has validation and return proper data with proper information in json format
    """
    # if query parameter of destination empty, it will redirect to root url
    if request.args.get('destination') == '':
        return redirect('/')
    # if there's no destination query parameter, it will render page to input destination
    if request.args.get('destination') == None:
        write_log('DESTINATION_REQUEST', {'message': 'access page'}, 200, 'Request')
        return render_template('index.html')
    
    # get destination value
    destination: str = request.args.get('destination')
    write_log('DESTINATION_REQUEST', {'message': 'send destinatnion', 'destination': destination}, 200, 'Request')
    
    # request geolocation of destination
    destination_location: tuple = geo.get_location(destination)

    # if destination location not found it will return 404
    if destination_location[-1] == False:
        response: dict = {'message': 'location not found', 'status': 0}
        write_log('DESTINATION_RESPONSE', response, 404)
        return jsonify(response), 404
    
    # get distance between origin and destination
    distance_result: tuple = geo.get_distance(destination_location[1])
    
    # if distance too far or not found will return 404
    if distance_result[-1] == False and distance_result[-1] is not 0:
        response: dict = {'message': 'distance not found', 'status': 2}
        write_log('DESTINATION_RESPONSE', response, 404)
        return jsonify(response), 404

    # split the distance_result tuple into distance and duration in meters and seconds
    distance: int
    duration: int
    distance, duration = distance_result

    # check if destination inside the origin, if True, it will run code below
    is_inside: bool = geo.is_inside(destination)
    if is_inside:
        response: dict = {'message': 'the destination inside in origin\'s area', 'status': 3}
        write_log('DESTINATION_RESPONSE', response, 200)
        return jsonify(response), 200

    # return the distance and duration value with 200 http code
    response = {'data':{'distance': distance, 'duration': duration}, 'message': 'success', 'status':1}
    write_log('DESTINATION_RESPONSE', response, 200)

    return jsonify(response), 200

@geo_bp.errorhandler(404)
def page_not_found(e) -> tuple:
    """
        it will render if user got invalid route
    """
    return render_template('404.html'), 404

def write_log(log_name, data, status, mode='Response') -> None:
    """
        this will write the log to logs/ directory
        it require the data, http status code, and mode (request or response)
    """
    file_log_name: str = f'{str(date.today())}.log'
    log_location: str = f'logs/{file_log_name}'
    timestamp: str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    log = {log_name: {mode: data, 'status': status}}
    # Write log
    with open(log_location, 'a+') as file:
        file.write(f'[{timestamp}] LOG:{log}\n')