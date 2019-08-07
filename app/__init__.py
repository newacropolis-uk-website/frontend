import os
import re

from flask import Flask, current_app, jsonify, make_response, render_template, request, session
from flask_wtf.csrf import CSRFProtect, CSRFError
import textile

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

def _is_admin_user():
    user = session['user']
    return 'admin' in user.get('access_area') or user.get('access_area') == 'admin'


def _get_course_details(topic):
    details = {}
    with open("app/templates/course_details/" + topic + ".txt", "rb") as f:
        details['text'] = f.read()
    details['html'] = textile.textile(details['text'])
    return details


def _get_summary_course_details(topic):
    with open("app/templates/course_details/" + topic + ".txt", "rb") as f:
        details = f.read(current_app.config['SUMMARY_LIMIT'])

    # ignore the first line as its the header
    details = ' '.join(details.split('\n')[1:])

    # ignore the last word in case it was split
    details = ' '.join(details.split(' ')[:-1])

    html_tag_pattern = r'<.*?>'
    clean_details = re.sub(html_tag_pattern, '', textile.textile(details))

    return clean_details


def init_app(app):
    app.jinja_env.globals['API_BASE_URL'] = app.config['API_BASE_URL']
    app.jinja_env.globals['get_email'] = _get_email
    app.jinja_env.globals['get_users_need_access'] = _get_users_need_access
    app.jinja_env.globals['is_admin_user'] = _is_admin_user
    app.jinja_env.globals['user_has_permissions'] = _user_has_permissions
    app.jinja_env.globals['get_course_details'] = _get_course_details
    app.jinja_env.globals['get_summary_course_details'] = _get_summary_course_details

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

    @app.errorhandler(CSRFError)
    def handle_csrf(err):
        app.logger.warning('csrf.error_message: {}'.format(err))
        app.logger.warning(
            'csrf.invalid_token: Aborting request, user_id: {}'.format(session['user']['id'])
        )

        resp = make_response(render_template(
            "errors/400.html",
            message=['Something went wrong, please go back and try again.']
        ), 400)
        return useful_headers_after_request(resp)


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


def useful_headers_after_request(response):
    response.headers.add('X-Frame-Options', 'deny')
    response.headers.add('X-Content-Type-Options', 'nosniff')
    response.headers.add('X-XSS-Protection', '1; mode=block')
    response.headers.add('Content-Security-Policy', (
        "default-src 'self' {} 'unsafe-inline';"
        "script-src 'self' {} *.google-analytics.com 'unsafe-inline' 'unsafe-eval' data:;"
        "connect-src 'self' *.google-analytics.com;"
        "object-src 'self';"
        "font-src 'self' {} data:;"
    ))
    if 'Cache-Control' in response.headers:
        del response.headers['Cache-Control']
    response.headers.add(
        'Cache-Control', 'no-store, no-cache, private, must-revalidate')
    return response
