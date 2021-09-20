#!/usr/bin/python3
'''API Module
'''
from flask import Blueprint


app_views = Blueprint('app_views',
                      __name__, url_prefix='/api/v1')


import api.v1.views.index
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.states import *
