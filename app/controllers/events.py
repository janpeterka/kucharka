# import datetime

# from flask import redirect, url_for, request
# from flask_classful import route
from flask_security import login_required

# from app.helpers.formaters import parse_date

# from app.models.daily_plans import DailyPlan
from app.models.events import Event

from app.helpers.extended_flask_view import ExtendedFlaskView


class EventsView(ExtendedFlaskView):
    decorators = [login_required]
