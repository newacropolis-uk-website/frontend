from flask import current_app, render_template
from random import randint

from app.main import main
from app.main.views import requires_auth
from app import api_client


@main.route('/')
def index():
    return render_template(
        'views/home.html'
    )


@main.route('/new_home')
def index1():
    events = api_client.get_events_in_future()[:3]

    articles = api_client.get_articles_summary()
    index = randint(0, len(articles) - 1)
    return render_template(
        'views/home1.html',
        images_url=current_app.config['IMAGES_URL'],
        article=articles[index],
        events=events
    )
