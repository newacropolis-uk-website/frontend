import pytest
from bs4 import BeautifulSoup
from flask import json, url_for, request

from tests.conftest import AUTH_USERNAME, AUTH_PASSWORD


class WhenAccessingHomePage(object):

    def it_shows_list_of_available_pages(self, client, mocker):
        response = client.get(url_for(
            'main.index'
        ))
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        assert page.find('h2').text == 'New Acropolis UK'


class WhenAccessingSpeakersPage(object):

    def it_shows_list_of_speakers(self, client, mocker, logged_in):
        mocker.patch(
            "app.clients.api_client.ApiClient.get_speakers",
            return_value=[
                {
                    "title": "Mr",
                    "name": "Test",
                    "alternate_names": "Dr Test"
                }
            ]
        )

        response = client.get(url_for(
            'main.speakers'
        ))
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        assert page.find('li').text == 'Mr Test  (Dr Test)'


class WhenAccessingVenuesPage(object):

    def it_shows_list_of_venues(self, client, mocker, logged_in):
        mocker.patch(
            "app.clients.api_client.ApiClient.get_venues",
            return_value=[
                {
                    "name": "London",
                    "address": "19 Test Terrace, N1",
                    "directions": "<div>Bus: 1, 5, 10 2 minutes walk</div>"
                }
            ]
        )

        response = client.get(url_for(
            'main.venues'
        ))
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        assert page.find('li').text == 'London: 19 Test Terrace, N1 Bus: 1, 5, 10 2 minutes walk'
