import pytest
import uuid
from bs4 import BeautifulSoup
from flask import json, url_for, request


class WhenAccessingHomePage(object):
    def it_should_future_events(self, client, sample_future_events, sample_articles_summary):
        response = client.get(url_for(
            'main.index'
        ))
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        content = page.find("h4", {"class": "card-title"}).string

        intro_course = [e for e in sample_future_events if e['event_type'] == 'Introductory Course'][0]

        assert content == intro_course['title']

    def it_should_show_future_events_in_carousel(self, client, sample_future_events, sample_articles_summary):
        response = client.get(url_for(
            'main.index'
        ))

        other_events = []
        for event in sample_future_events:
            if event['event_type'] != 'Introductory Course':
                other_events.append(event)

        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        carousel_items = page.select(".carousel_info_text")
        for i, event in enumerate(sample_future_events):
            if event['event_type'] == 'Introductory Course':
                # expect the first event in the carousel to be an intro course
                assert carousel_items[0].text.strip() == "Courses starting January 2019"
            elif event['image_filename']:
                # expect the other events to be after an intro course if they have an image
                assert carousel_items[i + 1].text.strip() == other_events[i]['title']

    @pytest.mark.parametrize('div_class', ['.nav', '.footer_nav'])
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
