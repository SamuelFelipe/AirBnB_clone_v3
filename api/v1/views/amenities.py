#!/usr/bin/python3

'''

'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    '''list all amenities'''
    response = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(response)


@app_views.route('/amenities/<string:id>',
                 methods=['GET'], strict_slashes=False)
def amenities_by_id(id):
    '''return a amenity filtered by the id'''
    response = storage.get(Amenity, id)
    if response:
        return response.to_dict()
    abort(404)


@app_views.route('/amenities/<string:id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(id):
    '''remove a intance of amenity'''
    response = storage.get(Amenity, id)
    if response:
        response.delete()
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''create a new amenity'''
    info = request.get_json()
    if not info:
        abort(400, description='Not a JSON')
    elif not info.get('name'):
        abort(400, description='Missing name')

    new = Amenity(**info)
    new.save()
    return new.to_dict(), 201


@app_views.route('/amenities/<string:id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(id):
    '''Update a amenity'''
    amenity = storage.get(Amenity, id)
    info = request.get_json()
    if not info:
        abort(400, description='Not a JSON')
    elif not info.get('name'):
        abort(400, description='Missing name')
    if amenity:
        info.pop('id', None)
        info.pop('created_at', None)
        info.pop('updated_at', None)
        for key, val in info.items():
            setattr(amenity, key, val)
        amenity.save()
        return amenity.to_dict(), 200
    abort(404)
