#!/usr/bin/python3

'''

'''

from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(err):
    return storage.close()

@app.errorhandler(404)
def invalid_route(e):
    '''handler for 404 errors that returns a JSON-formatted'''
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=host, port=port, threaded=True)
