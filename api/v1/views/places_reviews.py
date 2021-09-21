#!/usr/bin/python3

'''

'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<string:id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(id):
    place = storage.get(Place, id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<string:id>', methods=['GET'], strict_slashes=False)
def get_review(id):
    rev = storage.get(Review, id)
    if not rev:
        abort(404)
    return rev.to_dict()


@app_views.route('/reviews/<string:id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(id):
    rev = storage.get(Review, id)
    if not rev:
        abort(404)
    rev.delete()
    storage.save()
    return {}, 200


@app_views.route('/places/<string:id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(id):
    place = storage.get(Place, id)
    info = request.get_json()
    if not place:
        abort(404)
    elif not info:
        abort(400, description='Not a JSON')
    if not info.get('user_id'):
        abort(400, description='Missing user_id')
    elif not info.get('text'):
        abort(400, description='Missing text')
    user = storage.get(User, info['user_id'])
    if not user:
        abort(404)
    info['place_id'] = id
    rev = Review(**info)
    rev.save()
    return rev.to_dict(), 201


@app_views.route('/reviews/<string:id>', methods=['PUT'], strict_slashes=False)
def update_review(id):
    rev = storage.get(Review, id)
    info = request.get_json()
    if not rev:
        abort(404)
    elif not info:
        abort(400, description='Not a JSON')
    for ig in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
        info.pop(ig, None)
    for key, val in info.items():
        setattr(rev, key, val)
    return rev.to_dict(), 200
