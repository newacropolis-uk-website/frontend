import pytest
from bs4 import BeautifulSoup
from flask import json, url_for, request

from mock import MagicMock


class WhenAccessingHomePage(object):

    def it_shows_list_of_available_pages(self, client, mocker):
        response = client.get(url_for(
            'main.index'
        ))
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        assert page.find('h2').text == 'New Acropolis UK'


class WhenAccessingSpeakersPage(object):

    @pytest.mark.skip()
    def it_shows_list_of_speakers(self, client, mocker):
        class Request(object):
            class Authorization(object):
                username = "na"
                password = "newacropolis"
            authorization = Authorization
        mocker.patch("app.main.views.request", Request)

        response = client.get(url_for(
            'main.speakers'
        ))
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        assert False
