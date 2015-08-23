import time
from threading import Thread

from flask import Blueprint, render_template

from extensions import socketio


map_blueprint = Blueprint('map_blueprint', __name__,
                          template_folder="templates")


@map_blueprint.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on_error_default
def default_error_handler(e):
    pass
