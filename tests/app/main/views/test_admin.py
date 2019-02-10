from flask import url_for
from mock import Mock
import pytest

from bs4 import BeautifulSoup
from app.config import Config

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


def mock_sessions(mocker, session_dict={}):
    mocker.patch('app.session', session_dict)
    mocker.patch('app.main.views.session', session_dict)
    mocker.patch('app.main.views.admin.session', session_dict)
    mocker.patch('app.main.views.os.environ', session_dict)


@pytest.fixture
def access_areas():
    access_areas = ['{}{}'.format(a.capitalize(), 's' if a != 'shop' else '')
                    for a in Config.ACCESS_AREAS if a != 'admin']
    access_areas.append('Users')
    return access_areas


class WhenAccessingAdminPagesWithoutLoggingIn(object):

    def it_redirects_to_google_auth(self, client, mocker):
        mock_oauth2session(mocker, 'http://auth_url')

        mock_sessions(mocker)

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
        mock_sessions(mocker, session_dict)

        mocker.patch('app.main.views.os.environ', {})
        mocker.patch('app.main.views.api_client.get_user', return_value=Mock())

        response = client.get(url_for(
            'main.callback'
        ))
        assert response.status_code == 302
        assert session_dict['user_profile'] == {'name': 'test user', 'email': 'test@example.com'}


class WhenAccessingAdminPagesAfterLogin(object):

    def it_shows_all_areas_for_admin(self, client, mocker, access_areas):
        session_dict = {
            'user': {
                'access_area': 'admin'
            },
            'user_profile': {
                'name': 'test name',
                'email': 'test@example.com'
            }
        }
        users = [
            {
                'access_area': 'admin'
            }
        ]
        mock_sessions(mocker, session_dict)
        mocker.patch('app.api_client.get_users', return_value=users)

        response = client.get(url_for(
            'main.admin'
        ), follow_redirects=True)

        assert response.status_code == 200

        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

        areas = page.select('#content .row div')
        assert len(areas) == 8

        area_strs = [a.text.strip() for a in areas]
        assert set(access_areas) == set(area_strs)

    @pytest.mark.parametrize('areas', [
        'email,', 'email,event', 'event,report,article'
    ])
    def it_restricts_areas_for_non_admin(self, client, mocker, areas):
        session_dict = {
            'user': {
                'access_area': areas
            },
            'user_profile': {
                'name': 'test name',
                'email': 'test@example.com'
            }
        }
        users = [
            {
                'access_area': areas
            }
        ]
        mock_sessions(mocker, session_dict)
        mocker.patch('app.api_client.get_users', return_value=users)

        response = client.get(url_for(
            'main.admin'
        ), follow_redirects=True)

        assert response.status_code == 200

        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

        _areas = page.select('#content .row div')
        areas = ["{}s".format(a.capitalize()) for a in areas.split(',') if a]
        assert len(_areas) == len(areas)

        area_strs = [a.text.strip() for a in _areas]
        assert set(area_strs) == set(areas)
