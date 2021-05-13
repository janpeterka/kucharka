from flask import request, redirect, url_for
from flask_security import login_required, current_user

from app.helpers.extended_flask_view import ExtendedFlaskView

from app.models.ingredients import Ingredient


class DashboardView(ExtendedFlaskView):
    decorators = [login_required]

    @login_required
    def before_index(self):
        self.ingredients = [
            i for i in current_user.ingredients if i not in Ingredient.load_all_public()
        ]

    def index(self):
        return self.template("dashboard/dashboard.html.j2")

    def show(self, **kwargs):
        return redirect(url_for("DashboardView:index"))

    def post(self):
        return redirect(
            url_for("DashboardView:index", selected_diet_id=request.form["select_diet"])
        )
