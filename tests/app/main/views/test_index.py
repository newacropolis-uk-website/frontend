import pytest
import uuid
from bs4 import BeautifulSoup
from flask import json, url_for, request


class WhenAccessingHomePage(object):
    def it_should__display_banner_text(self, client, mocker):
        response = client.get(url_for(
            'main.index'
        ))
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        content = page.find("div", {"class": "banner_findoutmore"}).string
        assert content == 'FIND OUT MORE'


class WhenAccessingHomePage(object):
    def it_should_future_events(self, client, sample_future_events, sample_articles_summary):
        response = client.get(url_for(
            'main.index'
        ))
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        content = page.find("div", {"class": "whatson_block_subheading"}).string
        assert content == sample_future_events[0]['title']

    @pytest.mark.parametrize('div_class', ['.header', '.footer'])
    def it_shows_list_of_available_pages_on_header_and_footer(
        self, client, sample_future_events, sample_articles_summary, div_class
    ):
        expected_link_text = ['E-shop', 'Resources', 'Whats on', 'What we offer', 'About']
        response = client.get(url_for(
            'main.index'
        ))
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

        selected_div = page.select_one(div_class)
        for i, li in enumerate(selected_div.select('li a')):
            assert li.text == expected_link_text[i]
