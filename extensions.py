import indicoio
from redis import StrictRedis
from flask.ext import assets
from flask.ext.socketio import SocketIO
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config
import local_settings


env = assets.Environment()
socketio = SocketIO()
redis = StrictRedis(host=config.REDIS_HOST)

indicoio.config.api_key = local_settings.INDICO_API_KEY

engine = create_engine(local_settings.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
