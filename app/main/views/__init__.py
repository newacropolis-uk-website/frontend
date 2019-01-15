import os

from functools import wraps
from flask import current_app, redirect, request, Response, session, url_for
import requests
from requests_oauthlib import OAuth2Session

from app.main import main

# OAuth endpoints given in the Google API documentation
authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
token_url = "https://www.googleapis.com/oauth2/v4/token"
user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
scope = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ]


def check_auth(username, password):
    return username == current_app.config['AUTH_USERNAME'] and password == current_app.config['AUTH_PASSWORD']


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def requires_google_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get('oauth_token')
        if not token:
            return google_login()
        return f(*args, **kwargs)
    return decorated


def google_login():
    google = OAuth2Session(
                current_app.config['GOOGLE_OAUTH2_CLIENT_ID'],
                scope=scope,
                redirect_uri=current_app.config['GOOGLE_OAUTH2_REDIRECT_URI']
            )
    authorization_url, state = google.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    session['source_url'] = request.url

    return redirect(authorization_url)


@main.route("/oauth2callback", methods=["GET"])
def callback():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = current_app.config['OAUTHLIB_INSECURE_TRANSPORT']

    google = OAuth2Session(
                current_app.config['GOOGLE_OAUTH2_CLIENT_ID'],
                state=session['oauth_state'],
                redirect_uri=current_app.config['GOOGLE_OAUTH2_REDIRECT_URI']
            )

    token = google.fetch_token(
                token_url,
                client_secret=current_app.config['GOOGLE_OAUTH2_CLIENT_SECRET'],
                authorization_response=request.url
            )

    session['oauth_token'] = token

    auth_google = OAuth2Session(current_app.config['GOOGLE_OAUTH2_CLIENT_ID'], token=session['oauth_token'])

    profile = auth_google.get(user_info_url).json()

    # store profile in session to use later
    session['user_profile'] = profile
    print(profile)

    return redirect(session.pop('source_url', url_for('.admin')))
