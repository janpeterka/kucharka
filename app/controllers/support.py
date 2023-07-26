from flask import redirect, url_for
from flask import render_template as template
from flask_security import roles_required

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

    @route("login")
    def passwordless_login(self):
        return template("support/passwordless_login.html.j2")

    @route("register")
    def passwordless_register(self):
        return template("support/passwordless_register.html.j2")

    @route("passwordless")
    def passwordless(self):
        return redirect(url_for("SupportView:passwordless_register"))

    @roles_required("admin")
    @route("components")
    def components(self):
        return template("support/components.html.j2")
