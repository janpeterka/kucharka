from flask import redirect
from flask import render_template as template

from flask_classful import FlaskView, route


class SupportView(FlaskView):
    @route("terms")
    def terms(self):
        return template("support/terms.html.j2")

    @route("privacy")
    def privacy(self):
        return template("support/privacy.html.j2")

    @route("facebook")
    def facebook_redirect(self):
        return redirect("https://www.facebook.com/navarit.skaut")

    def flashing(self):
        from flask import get_flashed_messages, render_template, jsonify

        flashes = [
            render_template(
                "base/_flash.html.j2", category=category, message=message
            )
            for category, message in get_flashed_messages(with_categories=True)
        ]

        return jsonify(flashes)
