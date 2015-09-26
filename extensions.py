from flask.ext import assets
from flask.ext.socketio import SocketIO
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()
env = assets.Environment()
socketio = SocketIO()
