#!/usr/bin/python3

'''

'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    '''list all users'''
    list_user = [user.to_dict() for user in storage.all(User).values()]
    return list_user


@app_views.route('/users/<string:id>', methods=['GET'], strict_slashes=False)
def get_user(id):
    '''get a user by the id'''
    user = storage.get(User, id)
    if not user:
        abort(404)
    return user.to_dict()


@app_views.route('/users/<string:id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(id):
    '''delete a user'''
    user = storage.get(User, id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return {}, 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''create a user'''
    info = request.get_json()
    if not info:
        abort(400, description='Not a JSON')
    if not info.get('email'):
        abort(400, description='Missing email')
    elif not info.get('password'):
        abort(400, description='Missing password')
    new = User(**info)
    storage.save()
    return new.to_dict(), 201


@app_views.route('/users/<string:id>', methods=['PUT'], strict_slashes=False)
def update_user(id):
    '''Update a user'''
    info = request.get_json()
    if not info:
        abort(400, description='Not a JSON')
    user = storage.get(User, id)
    if not user:
        abort(404)
    info.pop('id', None)
    info.pop('email', None)
    info.pop('created_at', None)
    info.pop('updated_at', None)
    for key, val in info.items():
        setattr(user, key, val)
    user.save()
    return user.to_dict(), 200
