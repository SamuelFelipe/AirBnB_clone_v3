#!/usr/bin/python3

'''
main file from the api
'''

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', strict_slashes=False)
def status():
    '''return the api status'''
    return {'status': 'OK'}


@app_views.route('/stats', strict_slashes=False)
def count():
    '''return an item count'''
    count = {}
    for name, cls in classes.items():
        count[name] = storage.count(cls)
    return count
