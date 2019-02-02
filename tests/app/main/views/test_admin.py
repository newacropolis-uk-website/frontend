from flask import url_for


def mock_oauth2session(mocker, auth_url):

    class MockOAuth2Session:
        def __init__(*args, **kwargs):
            pass

        def authorization_url(self, url):
            return auth_url, 'state'

        def fetch_token(*args, **kwargs):
            return 'token'

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
        mocker.patch('app.main.views.session', session_dict)
        mocker.patch('app.main.views.admin.session', session_dict)
        mocker.patch('app.main.views.os.environ', {})

        response = client.get(url_for(
            'main.callback'
        ), follow_redirects=True)
        assert response.status_code == 200
        assert session_dict['user_profile'] == {'name': 'test user', 'email': 'test@example.com'}
