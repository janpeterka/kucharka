from flask import request, redirect, url_for
from flask_security import login_required
from flask_classful import route

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.form import create_form

from app.models import Event, Attendee
from app.forms import AttendeeForm


class AttendeeView(HelperFlaskView):
    decorators = [login_required]
