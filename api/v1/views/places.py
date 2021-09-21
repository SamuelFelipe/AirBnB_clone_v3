#!/usr/bin/python3

'''

'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:id>/places',
                 methods=['GET'], strict_slashes=False)
def get_city_places(id):
    '''get all the places in a city'''
    city = storage.get(City, id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<string:id>', methods=['GET'], strict_slashes=False)
def get_place(id):
    '''get a place by id'''
    place = storage.get(Place, id)
    if not place:
        abort(404)
    return place.to_dict()


@app_views.route('/places/<string:id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place(id):
    '''delete a place'''
    place = storage.get(Place, id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return {}, 200


@app_views.route('/cities/<string:id>/places',
                 methods=['POST'], strict_slashes=False)
def new_place(id):
    '''create a place'''
    info = request.get_json()
    if not info:
        abort(400, description='Not a JSON')
    city = storage.get(City, id)
    if not city:
        abort(404)
    if not info.get('user_id'):
        abort(400, description='Missing user_id')
    elif not info.get('name'):
        abort(400, description='Missing name')
    user = storage.get(User, info['user_id'])
    if not user:
        abort(404)
    info['city_id'] = id
    new = Place(**info)
    new.save()
    return new.to_dict(), 201


@app_views.route('/places/<string:id>', methods=['PUT'], strict_slashes=False)
def update_place(id):
    '''Update a place'''
    place = storage.get(Place, id)
    if not place:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, description='Not a JSON')
    for remove in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
        info.pop(remove, None)
    for key, val in info.items():
        setattr(place, key, val)
    return place.to_dict(), 200
