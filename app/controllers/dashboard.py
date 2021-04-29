from flask import request, redirect, url_for, flash
from flask_login import current_user, login_required

from app.helpers.extended_flask_view import ExtendedFlaskView


class DashboardView(ExtendedFlaskView):
    decorators = [login_required]

    def index(self):
        return self.template("dashboard/dashboard.html.j2")

    def show(self, **kwargs):
        return redirect(url_for("DashboardView:index"))

    def post(self):
        return redirect(
            url_for("DashboardView:index", selected_diet_id=request.form["select_diet"])
        )
