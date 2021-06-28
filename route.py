from os import write
from re import A
from flask import (Blueprint, request)
from flask import jsonify
from flask.templating import render_template
from config import Config
import requests
from geo import Geo
import logging
from datetime import date, datetime

geo_bp = Blueprint('geo_bp', __name__)
geo = Geo()

@geo_bp.route('/')
def index() -> dict:
    """

    """
    if request.args.get('destination') == None:
        write_log({'message': 'access page'}, 200, 'Request')
        return render_template('index.html')
    origin: str = 'Moscow%20Ring%20Road%20'
    destination: str = request.args.get('destination')
    write_log({'message': 'send destinatnion', 'destination': destination}, 200, 'Request')
    
    origin_location: tuple = Geo.get_location(origin)
    destination_location: tuple = Geo.get_location(destination)
    if destination_location[-1] == False:
        response: dict = {'message': 'location not found', 'status': 0}
        write_log(response, 404)
        return jsonify(response), 404
    
    distance_result = Geo.get_distance(origin_location[1], destination_location[1])
    
    if distance_result[-1] == False and distance_result[-1] is not 0:
        response: dict = {'message': 'distance not found', 'status': 2}
        write_log(response, 404)
        return jsonify(response), 404
    distance: int
    duration: int
    distance, duration = distance_result

    is_inside: bool = geo.is_inside(origin, destination)
    if is_inside:
        response: dict = {'message': 'the destination inside in origin\'s area', 'status': 3}
        write_log(response, 200)
        return jsonify(response), 200

    response = {'data':{'distance': distance, 'duration': duration}, 'message': 'success', 'status':1}
    write_log(response, 200)

    return jsonify(response), 200

@geo_bp.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

def write_log(data, status, mode='Response'):
    log_name: str = f'{str(date.today())}.log'
    log_location: str = f'logs/{log_name}'
    timestamp: str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    log = {mode: data, 'status': status}
    # Write log
    with open(log_location, 'a+') as file:
        file.write(f'[{timestamp}] LOG:{log}\n')