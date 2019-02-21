from flask import Flask, current_app, render_template, request
from random import randint
from forms import ContactForm

from app.main import main
from app import api_client


app = Flask(__name__)
app.secret_key = 'development key'

@main.route('/', methods=['GET', 'POST'])
def index():
    events = api_client.get_events_in_future(approved_only=True)
    for event in events:
        if event['event_type'] == 'Introductory Course':
            event['carousel_text'] = 'Courses starting {}'.format(event['event_monthyear'])

    articles = api_client.get_articles_summary()
    index = randint(0, len(articles) - 1)
    form = ContactForm()
    if request.method == 'POST':
        return render_template(
            'views/subscription.html',
            images_url=current_app.config['IMAGES_URL'],
            main_article=articles[index],
            articles=articles,
            events=events,
            current_page='',
            form=form
        )
    elif request.method == 'GET':
        return render_template(
            'views/home.html',
            images_url=current_app.config['IMAGES_URL'],
            main_article=articles[index],
            articles=articles,
            events=events,
            current_page='',
            form=form
        )

@main.route('/about')
def about():
    events = api_client.get_events_in_future(approved_only=True)
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


@main.route('/subscription')
def subscription():
    return render_template(
        'views/subscription.html',
    )
