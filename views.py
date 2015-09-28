from flask import Blueprint, current_app, render_template
from extensions import socketio

from constants import CANDIDATES
from twitter import TwitterStream


map_blueprint = Blueprint('map_blueprint', __name__,
                          template_folder="templates")

thread = None


@map_blueprint.route('/')
def index():
    global thread
    if thread is None:
        with current_app.app_context():
            thread = TwitterStream(
                current_app, socketio=socketio
            ).create_stream(CANDIDATES)
            thread.start()
    return render_template('index.html')


@socketio.on('tweet', namespace="/test")
def handle_message(message=None):
    import pdb; pdb.set_trace()
    print('received message: ' + message)


@socketio.on_error_default
def default_error_handler(e):
    pass
