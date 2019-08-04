from flask import Blueprint

main = Blueprint('main', __name__)  # noqa

from app.main.views import (  # noqa
    index, api, subscription
)

from app.main.views.admin import admin  # noqa
from app.main.views.admin import events  # noqa
from app.main.views.admin import emails  # noqa
