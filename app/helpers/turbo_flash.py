def turbo_flash(message):
    from app import turbo
    from flask import render_template as template

    return turbo.stream(
        turbo.replace(
            template("base/_turbo_flashing.html.j2", message=message, category="error"),
            target="turbo-flash",
        )
    )
