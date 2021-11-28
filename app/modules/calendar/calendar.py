#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask import Blueprint, make_response
from icalendar import Calendar, Event


calendar_blueprint = Blueprint(
    "calendar", __name__, url_prefix="/calendar", template_folder="templates"
)


def generate_ical_response(events):
    ical = generate_ical(events)
    response = make_response(ical)
    response.headers["Content-Disposition"] = "attachment; filename=calendar.ics"

    return response


def generate_ical(events):
    calendar = Calendar()
    calendar.add("prodid", "-//Akce//skautskakucharka.cz//")
    calendar.add("version", "2.0")

    for event in events:
        ical_event = _event_to_ical(event)
        calendar.add_component(ical_event)

    return calendar.to_ical()


def _event_to_ical(event):
    ical_event = Event()

    ical_event.add("summary", event.name)
    ical_event.add("uid", event.id)
    ical_event.add("dtstart", event.date_from)
    ical_event.add("dtend", event.date_to)
    ical_event.add("dtstamp", datetime.now())

    return ical_event
