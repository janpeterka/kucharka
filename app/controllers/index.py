from flask import redirect, url_for
from flask import render_template as template

from flask_classful import FlaskView, route
from flask_login import current_user


class IndexView(FlaskView):
    route_base = "/"

    def index(self):
        print("index")
        if current_user.is_authenticated:
            print("to dash")
            return redirect(url_for("DashboardView:index"))
        else:
            print("to index")
            return template("index/index.html.j2")

    @route("about")
    @route("about/")
    def about(self):
        return template("index/index.html.j2")
