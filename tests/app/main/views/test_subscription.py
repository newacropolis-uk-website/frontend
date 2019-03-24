from flask import url_for
from bs4 import BeautifulSoup

from tests.conftest import mock_sessions

class SubscriptionFormTests:
    def it_shows_email(self, client, mocker):
        email = [
            {
                'email': 'test@test.com'
            },
        ]

        mocker.patch('app.api_client.get_subscription_email', return_value=email)

        mock_sessions(mocker)
        response = client.get(url_for(
            'main.subscription'
        ), follow_redirects=True)

        assert response.status_code == 200

        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        email = page.select("h4").string

        assert email == "test@test.com"
