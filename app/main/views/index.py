from flask import render_template

from app.main import main
from app.main.views import requires_auth
from app import api_client


@main.route('/')
def index():
    return render_template(
        'views/home.html'
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
        'views/events_past_year.html',
        events=events,
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
