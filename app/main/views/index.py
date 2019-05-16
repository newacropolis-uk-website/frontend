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
        events=events,
        current_page=''
    )

@main.route('/about')
def about():
    events = api_client.get_events_in_future()
    for event in events:
        if event['event_type'] == 'Introductory Course':
            event['carousel_text'] = 'Courses starting {}'.format(event['event_monthyear'])

    articles = api_client.get_articles_summary()
    index = randint(0, len(articles) - 1)
    return render_template(
        'views/about.html',
        images_url=current_app.config['IMAGES_URL'],
        main_article=articles[index],
        articles=articles,
        events=events,
        current_page='about'
    )

@main.route('/resources')
def resources():
    return render_template(
        'views/resources.html',
        current_page='resources'
    )


@main.route('/whats-on')
def whats_on():
    return render_template(
        'views/whats_on.html',
        current_page='whats-on'
    )


@main.route('/what-we-offer')
def what_we_offer():
    return render_template(
        'views/what_we_offer.html',
        current_page='what-we-offer'
    )


@main.route('/e-shop')
def e_shop():
    return render_template(
        'views/e-shop.html',
        current_page='e-shop'
    )
