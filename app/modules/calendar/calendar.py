#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask import make_response
from icalendar import Calendar, Event


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
    ical_event.add("dtstart", event.starts_at)
    ical_event.add("dtend", event.ends_at)
    ical_event.add("dtstamp", datetime.now())
    ical_event.add("description", event.url)

    return ical_event
