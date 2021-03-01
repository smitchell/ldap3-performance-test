#!/usr/bin/env python3
import logging
import sys

from confuse import Configuration
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

config_root = 'gateway_service'


def app_register_blueprints(app):
    with app.app_context():
        from .api import gateway_api
        # swagger specific
        SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
            app.config['swagger']['ui_url'],
            app.config['swagger']['api_url'],
            config={
                'app_name': "Gateway Service"
            }
        )
        app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=app.config['swagger']['ui_url'])
        # end swagger specific
        app.register_blueprint(gateway_api.get_blueprint())


def app_logging_config(app):
    with app.app_context():
        logging.basicConfig(level=logging.WARNING,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message).4096s',
                            datefmt='%m-%d %H:%M')
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message).1028s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        app.logger.setLevel(logging.INFO)


def app_init(app):
    CORS(app)
    config = Configuration(config_root, __name__)
    app.config['ldap_service_url'] = config['ldap_service_url'].get(str)
    app.config['swagger'] = config['swagger'].get(dict)
    app_register_blueprints(app)


app = Flask(__name__)
app_init(app)
app_logging_config(app)


@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)
