import pytest
import uuid
from bs4 import BeautifulSoup
from flask import json, url_for, request

from tests.conftest import AUTH_USERNAME, AUTH_PASSWORD


class WhenAccessingHomePage(object):
    def it_should__display_banner_text(self, client, mocker):
        response = client.get(url_for(
            'main.index'
        ))
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        content = page.find("div", {"class": "banner_findoutmore"}).string
        assert content == 'FIND OUT MORE'


class WhenAccessingHomePage(object):
    def it_should_display_header_content(self, client, mocker):
        response = client.get(url_for(
            'main.index'
        ))
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        content = page.find("div", {"class": "header_about"}).string
        assert content == 'About'

    def it_shows_list_of_available_pages(self, client, mocker):
        response = client.get(url_for(
            'main.index'
        ))
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        content = page.find("div", {"class": "footer_whatweoffer"}).string
        assert content == 'What we offer'
