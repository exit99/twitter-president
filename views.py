import json
# For flask-socketio.
from gevent import monkey
monkey.patch_all()
from threading import Thread

from flask import Blueprint, render_template

from constants import CANDIDATES
from extensions import socketio
from models import PresidentialCandidate


thread = None
map_blueprint = Blueprint('map_blueprint', __name__,
                          template_folder="templates")


@map_blueprint.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=PresidentialCandidate.subscribe)
        thread.start()
    ctx = {
        'namespace': PresidentialCandidate.namespace,
        'msg_name': PresidentialCandidate.msg_name,
        'map_data': json.dumps(PresidentialCandidate.current_map_data()),
        'candidates': CANDIDATES
    }
    return render_template('index2.html', **ctx)


@socketio.on('my event', namespace=PresidentialCandidate.namespace)
def test_message(message):
    """This must be here for socketio to work."""
    pass
