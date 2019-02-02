import uuid
from bs4 import BeautifulSoup
from flask import json, url_for, request
from mock import Mock


def mock_oauth2session(mocker, auth_url):

    class MockOAuth2Session:
        def __init__(*args, **kwargs):
            pass

        def authorization_url(self, url):
            return auth_url, 'mock_state'

        def fetch_token(*args, **kwargs):
            return 'mock_token'

        def get(self, url):

            class MockProfile:
                def json(self):
                    return {
                        'name': 'test user',
                        'email': 'test@example.com'
                    }

            return MockProfile()

    mocker.patch('app.main.views.OAuth2Session', MockOAuth2Session)


class WhenAccessingAdminPagesWithoutLoggingIn(object):

    def it_redirects_to_google_auth(self, client, mocker):
        mock_oauth2session(mocker, 'http://auth_url')

        mocker.patch('app.session', {})
        mocker.patch('app.main.views.session', {})
        mocker.patch('app.main.views.os.environ', {})

        response = client.get(url_for(
            'main.admin'
        ))
        assert response.status_code == 302
        assert response.location == 'http://auth_url'

    def it_stores_the_profile_in_session(self, client, mocker):
        mock_oauth2session(mocker, url_for('main.callback'))

        session_dict = {
            'oauth_state': 'state'
        }
        mocker.patch('app.session', session_dict)
        mocker.patch('app.main.views.session', session_dict)
        mocker.patch('app.main.views.admin.session', session_dict)
        mocker.patch('app.main.views.os.environ', {})
        mocker.patch('app.main.views.api_client.get_user', return_value=Mock())

        response = client.get(url_for(
            'main.callback'
        ), follow_redirects=True)
        assert response.status_code == 200
        assert session_dict['user_profile'] == {'name': 'test user', 'email': 'test@example.com'}
