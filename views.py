import time
from threading import Thread


from flask import Blueprint, render_template

from extensions import socketio


map_blueprint = Blueprint('map_blueprint', __name__,
                          template_folder="templates")


thread = None


def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        time.sleep(2)
        socketio.emit('message', {'broadcast': True})


@map_blueprint.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.start()
    return render_template('index.html')


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on_error_default
def default_error_handler(e):
    pass
