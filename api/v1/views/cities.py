#!/usr/bin/python3

'''

'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_state_cities(state_id):
    '''Retrieves the list of all City objects of a State'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    '''Retrieves a City object'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return city.to_dict()


@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city_by_id(city_id):
    '''delete a City object'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return {}, 200


@app_views.route('states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    '''create a city'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, description='Not a JSON')
    elif not info.get('name'):
        abort(400, description='Missing name')
    new = City(**info, state_id=state_id)
    new.save()
    return new.to_dict(), 201


@app_views.route('/cities/<string:city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''update a City object'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, description='Not a JSON')
    elif not info.get('name'):
        abort(400, description='Missing name')
    if city:
        info.pop('id', None)
        info.pop('created_at', None)
        info.pop('updated_at', None)
        for key, val in info.items():
            setattr(city, key, val)
        city.save()
        return city.to_dict(), 200
    abort(404)
