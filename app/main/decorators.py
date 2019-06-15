from flask import redirect, url_for
from functools import wraps


from app.main.forms import SubscriptionForm


def setup_subscription_form(func):
    @wraps(func)
    def _setup_subscription_form(*args, **kwargs):
        subscription_form = SubscriptionForm()

        if subscription_form.validate_on_submit():
            return redirect(url_for('main.subscription', email=subscription_form.email.data))

        kwargs['subscription_form'] = subscription_form

        return func(*args, **kwargs)
    return _setup_subscription_form
