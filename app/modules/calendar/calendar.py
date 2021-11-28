#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

from flask import render_template as template

calendar_blueprint = Blueprint(
    "calendar", __name__, url_prefix="/calendar", template_folder="templates"
)


def generate_ical(events):
    return template("calendar/ical.j2", events=events)
