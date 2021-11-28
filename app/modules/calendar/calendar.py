#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

# from flask import abort
from flask import render_template as template

calendar_blueprint = Blueprint(
    "calendar", __name__, url_prefix="/calendar", template_folder="templates"
)


@calendar_blueprint.route("/show/<calendar_hash>")
def show(calendar_hash):
    from app.models.events import Event

    events = Event.load_all()
    return _generate_ical(events)

    # from app.models.users import User

    # user = User.load_by_calendar_hash(calendar_hash)
    # if not user:
    #     abort(404)

    # ical = _generate_ical(user.events)
    # return ical


def _generate_ical(events):
    return template("calendar/ical.j2", events=events)
