import gevent
from flask import Blueprint, current_app, render_template
from extensions import socketio

from constants import CANDIDATES
from twitter import stream_api_connection


map_blueprint = Blueprint('map_blueprint', __name__,
                          template_folder="templates")


stream = stream_api_connection()
streams = []


@map_blueprint.route('/')
def index():
    if not streams:
        streams.append(stream.filter(track=[CANDIDATES], async=True))
    return render_template('index.html')


@socketio.on('tweet', namespace="/test")
def handle_message(message=None):
    import pdb; pdb.set_trace()
    print('received message: ' + message)


@socketio.on_error_default
def default_error_handler(e):
    pass
