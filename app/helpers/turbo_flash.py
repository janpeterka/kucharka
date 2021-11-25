from flask import session
from flask import render_template as template

from app import turbo


def turbo_flash(message, category=None):
    session["turbo_flash_message"] = message
    session["turbo_flash_message_category"] = category


def is_flash_in_session() -> bool:
    return "turbo_flash_message" in session


def turbo_flash_partial():

    message = session.get("turbo_flash_message", None)
    category = session.get("turbo_flash_message_category", None)

    if message:
        session.pop("turbo_flash_message")
        session.pop("turbo_flash_message_category")

        return turbo.append(
            template("base/_flash.html.j2", message=message, category=category),
            target="flashes",
        )
