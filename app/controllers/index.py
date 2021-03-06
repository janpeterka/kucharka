from flask import redirect, url_for
from flask import render_template as template

from flask_classful import FlaskView, route
from flask_security import current_user


class IndexView(FlaskView):
    route_base = "/"

    def index(self):
        if current_user.is_authenticated:
            return redirect(url_for("DashboardView:index"))
        else:
            return template("index/index.html.j2")

    @route("about")
    @route("about/")
    @route("o-kucharce")
    def about(self):
        return template("index/index.html.j2")

    @route("databaze")
    @route("databaze/")
    @route("recepty")
    @route("recepty/")
    def public_recipes(self):
        return redirect(url_for("PublicRecipeView:public_index"))

    @route("galerie")
    @route("galerie/")
    def gallery_public_recipes(self):
        return redirect(url_for("PublicRecipeView:gallery"))

    @route("tips")
    @route("tipy")
    def tips(self):
        return redirect(url_for("TipView:index"))

    @route("uptime")
    def uptime(self):
        return "OK"
