from flask import current_app, render_template
from random import randint

from app.main import main
from app import api_client


@main.route('/')
def index():
    events = api_client.get_events_in_future()
    for event in events:
        if event['event_type'] == 'Introductory Course':
            event['carousel_text'] = 'Courses starting {}'.format(event['event_monthyear'])

    articles = api_client.get_articles_summary()
    index = randint(0, len(articles) - 1)
    return render_template(
        'views/home.html',
        images_url=current_app.config['IMAGES_URL'],
        main_article=articles[index],
        articles=articles,
        events=events
    )


@main.route('/old')
def index0():
    return render_template(
        'views/home0.html'
    )
