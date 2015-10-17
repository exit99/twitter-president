# This patch is needed for flask-assets to work in development.
# Otherwise select.so.poll() throws an attribute error.
from gevent import monkey
monkey.patch_all()

import logging
import os

from flask import Flask
from flask.ext import assets

import config
import local_settings


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(config)
    app.config.from_object(local_settings)
    configure_logging(app)
    configure_extensions(app)
    configure_static(app)
    register_blueprints(app)
    return app


def configure_logging(app):
    logging.basicConfig(filename=app.config['LOGGING_FILE'],
                        level=logging.WARNING)


def configure_extensions(app):
    from extensions import socketio
    socketio.init_app(app)


def configure_static(app):
    from extensions import env
    env.init_app(app)
    with app.app_context():
        env.config['less_bin'] = app.config["LESS_BIN"]
        env.load_path = [
            os.path.join(os.path.dirname(__file__), 'bower_components'),
            os.path.join(os.path.dirname(__file__), 'static'),
        ]
    env.register(
        'js_all',
        assets.Bundle(
            'jquery/dist/jquery.min.js',
            'd3/d3.min.js',
            'topojson/topojson.js',
            'datamaps/dist/datamaps.usa.min.js',
            'socket.io-client/dist/socket.io.min.js',
            'lodash/lodash.js',
            'js/bootstrap.min.js',
            assets.Bundle(
                'coffee/maps.coffee',
                'coffee/pres_socket.coffee',
                filters=['coffeescript']
            ),
            output='js_all.js'
        )
    )
    env.register(
        'css_all',
        assets.Bundle(
            'css/bootstrap.min.css',
            assets.Bundle(
                'less/variables.less',
                'less/mixins.less',
                'less/freelancer.less',
                filters=['less']
            ),
            output='css_all.css'
        )
    )


def register_blueprints(app):
    from views import map_blueprint
    app.register_blueprint(map_blueprint)
