#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, make_response


calendar_blueprint = Blueprint(
    "calendar", __name__, url_prefix="/calendar", template_folder="templates"
)


def generate_ical(events):
    return render_template("calendar/ical.j2", events=events)


def generate_ical_response(events):
    ical = generate_ical(events)
    response = make_response(ical)
    response.headers["Content-Disposition"] = "attachment; filename=calendar.ics"

    return response
