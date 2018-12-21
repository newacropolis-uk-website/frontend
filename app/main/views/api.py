from flask import render_template
from six.moves.html_parser import HTMLParser

from app.main import main
from app.main.views import requires_auth
from app import api_client


@main.route('/api')
def api_test():
    return render_template(
        'views/api.html'
    )


@main.route('/speakers')
@requires_auth
def speakers():
    speakers = api_client.get_speakers()
    return render_template(
        'views/speakers.html',
        speakers=speakers
    )


@main.route('/venues')
@requires_auth
def venues():
    venues = api_client.get_venues()
    return render_template(
        'views/venues.html',
        venues=venues
    )


@main.route('/past_events')
def past_events():
    events = api_client.get_events_past_year()
    return render_template(
        'views/events.html',
        events=events,
        api_base_url=api_client.base_url
    )


@main.route('/future_events')
def future_events():
    events = api_client.get_events_in_future()

    return render_template(
        'views/events.html',
        events=_unescape_html(events, 'description'),
        api_base_url=api_client.base_url
    )


@main.route('/articles/summary')
def articles_summary():
    articles = api_client.get_articles_summary()
    return render_template(
        'views/articles_summary.html',
        articles=articles
    )


@main.route('/article/<uuid:id>')
def article(id):
    article = api_client.get_article(id)
    return render_template(
        'views/article.html',
        article=article
    )


def _unescape_html(items, field_name):
    h = HTMLParser()
    for item in items:
        item[field_name] = h.unescape(item[field_name])

    return items
