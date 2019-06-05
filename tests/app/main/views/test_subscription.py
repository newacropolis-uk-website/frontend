from flask import url_for
from bs4 import BeautifulSoup
from mock import Mock, call


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
        submitted_email = page.find('input')['value']

        assert submitted_email == "test@test.com"

    def it_shows_validation_error_when_empty(self, client, mocker, sample_future_events, sample_articles_summary):
        response = client.post(
            url_for('main.index'),
            follow_redirects=True)

        assert response.status_code == 200

        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        error = page.find("li", {"class": "error_text"}).text.strip()

        assert error == "This field is required."

    def it_shows_validation_for_invalid_email(self, client, mocker, sample_future_events, sample_articles_summary):
        response = client.post(
            url_for('main.index'),
            data={'email': 'test'},
            follow_redirects=True)

        assert response.status_code == 200

        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        error = page.find("li", {"class": "error_text"}).text.strip()

        assert error == "Invalid email address."

    def it_shows_error_on_failed_submit_to_api(self, client, mocker, sample_future_events, sample_articles_summary):
        class MockSubForm:
            class MockEmail:
                data = 'test@test.com'

                def __call__(self, **kwargs):
                    return 'mock_email'

            def __init__(self):
                self.email = self.MockEmail()

            def validate_on_submit(self):
                return True

        mocker.patch('app.main.views.subscription.SubscriptionForm', MockSubForm)

        response = client.post(url_for(
            'main.subscription',
            data={'email': 'test@test.com'}
        ), follow_redirects=True)

        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        error = page.find("li", {"class": "error_text"}).text.strip()
        assert error == "Failed to process email, please try again later"

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

        class MockAPIClient:
            def add_subscription_email(self):
                return [
                    {
                        "email": "test@test.com"
                    }
                ]

        mock_api_client = MockAPIClient()
        mock_api_client.add_subscription_email = Mock()
        mock_api_client.add_subscription_email.return_value = {'email': 'test@test.com'}
        mocker.patch('app.main.views.subscription.api_client', mock_api_client)

        mocker.patch('app.main.views.subscription.SubscriptionForm', MockSubForm)

        response = client.post(url_for(
            'main.subscription',
            data={'email': 'test@test.com'}
        ), follow_redirects=True)

        assert response.status_code == 200

        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        content = page.find("p", {"class": "card-text cardtextmulti dark_grey_txt"}).string
        intro_course = [e for e in sample_future_events if e['event_type'] == 'Introductory Course'][0]

        assert content == intro_course['title']

        assert mock_api_client.add_subscription_email.call_args == call(
            'test@test.com'
        )
