def turbo_flash(message, category=None):
    from flask import session

    session["turbo_flash_message"] = message


def turbo_flash_partial():
    from app import turbo
    from flask import session
    from flask import render_template as template

    if "turbo_flash_message" in session:
        message = session["turbo_flash_message"]
        session.pop("turbo_flash_message")

        return turbo.replace(
            template("base/_turbo_flashing.html.j2", message=message, category="error"),
            target="turbo-flash",
        )
    else:
        return None
