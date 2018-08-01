import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Blueprint, Flask, jsonify, session

from app.clients.api_client import ApiClient


__version__ = '0.0.1'

api_client = ApiClient()


def create_app(**kwargs):
    application = Flask(__name__)

    from app.config import configs

    environment_state = get_env(application)

    application.config.from_object(configs[environment_state])
    setup_config(application, configs[environment_state])

    application.config.update(kwargs)

    init_app(application)

    api_client.init_app(application)

    from app.main import main as main_blueprint
    application.register_blueprint(main_blueprint)

    return application


def init_app(app):
    @app.before_request
    def make_session_permanent():
        session.permanent = True

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    @app.errorhandler(Exception)
    def exception(error):
        print(error)
        app.logger.exception(error)
        # error.code is set for our exception types.
        # return jsonify(result='error', message=error.message), error.code or 500
        # return jsonify(result='error'), error.code or 500
        print(error)

    @app.errorhandler(404)
    def page_not_found(e):
        msg = e.description or "Not found"
        app.logger.exception(msg)
        return jsonify(result='error', message=msg), 404


def setup_config(application, config_class):
    application.config.from_object(config_class)


def get_env(app):
    if 'www-preview' in get_root_path(app):
        return 'preview'
    elif 'www-live' in get_root_path(app):
        return 'live'
    else:
        return os.environ.get('ENVIRONMENT', 'development')


def get_root_path(application):
    return application.root_path
