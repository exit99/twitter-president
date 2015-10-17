import indicoio
from flask.ext import assets
from flask.ext.socketio import SocketIO
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import local_settings


env = assets.Environment()
socketio = SocketIO()

indicoio.config.api_key = local_settings.INDICO_API_KEY

engine = create_engine(local_settings.SQLALCHEMY_DATABASE_URI, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
