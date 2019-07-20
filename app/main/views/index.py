from flask import current_app, render_template, redirect, url_for, request, jsonify
from random import randint
from app.main import main
from app import api_client
from app.main.decorators import setup_subscription_form
from app.main.forms import ContactForm
from app.clients.errors import HTTPError



@main.route('/', methods=['GET', 'POST'])
@setup_subscription_form
def index(**kwargs):
    events = api_client.get_events_in_future(approved_only=True)
    for event in events:
        if event['event_type'] == 'Introductory Course':
            event['carousel_text'] = 'Courses starting {}'.format(event['event_monthyear'])

    articles = api_client.get_articles_summary()
    index = randint(0, len(articles) - 1)

    contact_form = ContactForm()

    return render_template(
        'views/home.html',
        images_url=current_app.config['IMAGES_URL'],
        main_article=articles[index],
        articles=articles,
        events=events,
        current_page='',
        contact_form=contact_form,
        **kwargs
    )

@main.route('/about')
@setup_subscription_form
def about(**kwargs):
    contact_form = ContactForm()
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
        current_page='about',
        contact_form=contact_form,
        **kwargs
    )

@main.route('/resources')
@setup_subscription_form
def resources(**kwargs):
    contact_form = ContactForm()
    return render_template(
        'views/resources.html',
        current_page='resources',
        contact_form=contact_form,
        **kwargs
    )


@main.route('/whats-on')
@setup_subscription_form
def whats_on(**kwargs):
    contact_form = ContactForm()
    return render_template(
        'views/whats_on.html',
        current_page='whats-on',
        contact_form=contact_form,
        **kwargs
    )


@main.route('/what-we-offer')
@setup_subscription_form
def what_we_offer(**kwargs):
    contact_form = ContactForm()
    return render_template(
        'views/what_we_offer.html',
        current_page='what-we-offer',
        contact_form=contact_form,
        **kwargs
    )


@main.route('/e-shop')
@setup_subscription_form
def e_shop(**kwargs):
    contact_form = ContactForm()
    return render_template(
        'views/e-shop.html',
        current_page='e-shop',
        contact_form=contact_form,
        **kwargs
    )


@main.route('/_add_contact_details')
def _add_contact_details():
    name = request.args.get('name')
    if name:
        try:
            contact_details = api_client.add_contact_details(name)
            return jsonify(contact_details)
        except HTTPError as e:
            return jsonify({'error': e.message})
