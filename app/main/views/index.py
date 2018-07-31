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
