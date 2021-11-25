from flask import session, flash
from flask import render_template as template

from app import turbo


def turbo_flash(message, category=None):
    if turbo.can_stream():
        save_flash_to_session(message, category)
    else:
        flash(message, category)


def turbo_flash_partial(message, category):
    return turbo.replace(
        template("base/_flashing.html.j2", messages=[(category, message)]),
        target="flashes",
    )


def save_flash_to_session(message, category):
    session["turbo_flash_message"] = message
    session["turbo_flash_message_category"] = category


def remove_flash_from_session():
    session.pop("turbo_flash_message")
    session.pop("turbo_flash_message_category")


def is_flash_in_session() -> bool:
    return "turbo_flash_message" in session
