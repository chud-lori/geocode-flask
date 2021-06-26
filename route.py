from flask import (Blueprint, request)
from flask import jsonify
from flask.templating import render_template
from config import Config
import requests
from geo import Geo

geo_bp = Blueprint('geo_bp', __name__)
geo = Geo()

@geo_bp.route('/')
def index() -> dict:
    if request.args.get('destination') == None:
        return render_template('index.html')
    origin = 'Moscow%20Ring%20Road%20'
    location: str = request.args.get('destination')
    
    origin: tuple = Geo.get_location(origin)
    destination: tuple = Geo.get_location(location)
    if destination[-1] == False:
        return jsonify({'message': 'location not found', 'status': 0}), 404
    
    distance_result = Geo.get_distance(origin[1], destination[1])
    if distance_result[-1] == False:
        return jsonify({'message': 'distance not found', 'status': 2}), 404
    distance: int
    duration: int
    distance, duration = distance_result

    result = {'data':{'distance': distance, 'duration': duration}, 'message': 'success', 'status':1}

    return jsonify(result), 200

@geo_bp.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404