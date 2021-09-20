#!/usr/bin/python3

'''
Api management to the class State
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    '''return a list with all the states'''
    states = storage.all(State)
    responce = [obj.to_dict() for obj in states.values()]
    return jsonify(responce)


@app_views.route('/states/<string:id>', methods=['GET'], strict_slashes=False)
def state_by_id(id):
    '''return a state information'''
    state = storage.get(State, id)
    if state:
        return state.to_dict()
    abort(404)


@app_views.route('/states/<string:id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(id):
    '''delete a state'''
    state = storage.get(State, id)
    if state:
        state.delete()
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/states',
                 methods=['POST'], strict_slashes=False)
def post_state(state_id):
    '''Create a new state'''
    info = request.get_json()
    if not info:
        return 'Not a JSON\n', 400
    elif not info.get('name'):
        return 'Missing name\n', 400
    new = City(**info)
    new.save()
    return new.to_dict(), 201


@app_views.route('/states/<string:id>', methods=['PUT'], strict_slashes=False)
def update_state(id):
    '''Update a state'''
    state = storage.get(State, id)
    info = request.get_json()
    if not info:
        return 'Not a JSON', 400
    elif not info.get('name'):
        return 'Missing name\n', 400
    if state:
        info.pop('id', None)
        info.pop('created_at', None)
        info.pop('updated_at', None)
        for key, val in info.items():
            setattr(state, key, val)
        state.save()
        return state.to_dict(), 200
    abort(404)
