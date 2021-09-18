#!/usr/bin/python3

'''
main file from the api
'''

from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    '''return the api status'''
    return {'status': 'OK'}
