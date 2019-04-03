from flask import url_for
from bs4 import BeautifulSoup
"""
from mock import Mock
"""
"""
class MockAPIClient:
    def add_subscription_email(self):
        return [
            {
                "email": "test@test.com"
            }
        ]
"""

class WhenSubmittingSubscriptionForm(object):
    def it_displays_the_submitted_email(self, client, mocker, sample_future_events, sample_articles_summary):
        class MockSubForm:
            class MockEmail:
                data = 'test@test.com'

                def __call__(self, **kwargs):
                    return 'mock_email'

            def __init__(self):
                self.email = self.MockEmail()

            def validate_on_submit(self):
                return True

        mocker.patch('app.main.views.index.SubscriptionForm', MockSubForm)

        response = client.post(url_for(
            'main.index',
            data={'email': 'test@test.com'}
        ), follow_redirects=True)

        assert response.status_code == 200

        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        submitted_email = page.select_one('h4').string

        assert submitted_email == "Email: test@test.com"

    def it_shows_validation_error_when_empty(self, client, mocker, sample_future_events, sample_articles_summary):
        response = client.post(
            url_for('main.index'),
            follow_redirects=True)

        assert response.status_code == 200

        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

        assert page.find("li", {"class": "error_text"}).text.strip() == "This field is required."

    def it_shows_validation_for_invalid_email(self, client, mocker, sample_future_events, sample_articles_summary):
        response = client.post(
            url_for('main.index'),
            data={'email': 'test'},
            follow_redirects=True)

        assert response.status_code == 200

        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

        assert page.find("li", {"class": "error_text"}).text.strip() == "Invalid email address."

    """
    def it_submits_to_api(self, client, mocker, sample_future_events, sample_articles_summary):
        class MockSubForm:
            class MockEmail:
                data = 'test@test.com'

                def __call__(self, **kwargs):
                    return 'mock_email'

            def __init__(self):
                self.email = self.MockEmail()

            def validate_on_submit(self):
                return True

        mocker.patch('app.main.views.index.SubscriptionForm', MockSubForm)

        response = client.post(url_for(
            'main.index',
            data={'email': 'test@test.com'}
        ), follow_redirects=True)

        assert response.status_code == 200

        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        submitted_email = page.select_one('h4').string

        assert submitted_email == "Email: test@test.com"

        mock_api_client = MockAPIClient()
        mock_api_client.add_subscription_email = Mock()
        mock_api_client.add_subscription_email.return_value = {'email': 'test@test.com'}

        response = client.post(url_for(
            'main.subscription',
            data={'email': 'test@test.com'}
        ))

        assert response.status_code == 404
    """
