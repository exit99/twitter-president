from flask.ext import assets
from flask.ext.socketio import SocketIO

from twitter import TwitterThreadController


env = assets.Environment()
socketio = SocketIO()
thread_controller = TwitterThreadController()
