import logging
import os
from gevent import monkey
monkey.patch_all()

from flask import Flask
from flask.ext import assets

from extensions import env, socketio


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = 'secret!'
    app.config['REDIS_HOST'] = '127.0.0.1'
    configure_logging()
    app = configure_extensions(app)
    app = register_blueprints(app)
    return app


def configure_logging():
    logging.basicConfig()


def configure_extensions(app):
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
