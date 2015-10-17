import logging
import os

from flask import Flask
from flask.ext import assets

import local_settings


def create_app(threads=True):
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = 'secret!'
    app.config['REDIS_HOST'] = '127.0.0.1'
    app.config.from_object(local_settings)
    configure_logging(app)
    app = configure_extensions(app)
    app = register_blueprints(app)
    return app


def configure_logging(app):
    logging.basicConfig(filename=app.config['LOGGING_FILE'],
                        level=logging.WARNING)


def configure_extensions(app):
    from extensions import db, env, socketio
    db.init_app(app)
    socketio.init_app(app)
    env.init_app(app)
    with app.app_context():
        env.load_path = [
            os.path.join(os.path.dirname(__file__), 'bower_components')
        ]
    env.register(
        'js_all',
        assets.Bundle(
            'jquery/dist/jquery.min.js',
            'd3/d3.min.js',
            'topojson/topojson.js',
            'datamaps/dist/datamaps.usa.min.js',
            assets.Bundle(
                'coffee/map.coffee',
                'coffee/sockets.coffee',
                filters=['coffeescript']
            ),
            output='js_all.js'
        )
    )
    return app


def register_blueprints(app):
    from views import map_blueprint
    app.register_blueprint(map_blueprint)
    return app
