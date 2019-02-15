import os

from flask import Flask, jsonify, request, session
from flask_wtf.csrf import CSRFProtect

from app.clients.api_client import ApiClient
import requests_toolbelt.adapters.appengine

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()


__version__ = '0.0.1'

api_client = ApiClient()
csrf = CSRFProtect()


def create_app(**kwargs):
    application = Flask(__name__)
    from app.config import configs

    environment_state = get_env(application)

    csrf.init_app(application)
    application.config.from_object(configs[environment_state])
    setup_config(application, configs[environment_state])

    application.config.update(kwargs)

    use_gaesession(application)

    init_app(application)

    api_client.init_app(application)

    from app.main import main as main_blueprint
    application.register_blueprint(main_blueprint)

    return application


def _get_email():
    profile = session.get('user_profile')
    if profile:
        return profile['email']


def _get_users_need_access():
    users = [u for u in api_client.get_users() if not u['access_area']]
    return users


def _user_has_permissions(area):
    access_areas = session['user']['access_area'].split(',')
    if 'admin' in access_areas:
        return True
    return area in access_areas


def init_app(app):
    app.jinja_env.globals['get_email'] = _get_email
    app.jinja_env.globals['get_users_need_access'] = _get_users_need_access
    app.jinja_env.globals['user_has_permissions'] = _user_has_permissions

    @app.before_request
    def check_auth_required():
        if '/admin' in request.url and not session.get('user'):
            from app.main.views import google_login
            return google_login()

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


def use_gaesession(application):
    import gaesession
    application.session_interface = gaesession.GaeNdbSessionInterface(application)
