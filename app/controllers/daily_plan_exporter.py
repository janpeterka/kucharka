# import datetime

from flask import redirect, url_for, request
from flask import render_template as template

# from flask_classful import route
# from flask_login import current_user, login_required

# from app.helpers.formaters import parse_date

# from app.data.texts import texts

from app.models.daily_plans import DailyPlan

# from app.models.recipes import Recipe

from app.helpers.extended_flask_view import ExtendedFlaskView


class DailyPlanExporterView(ExtendedFlaskView):
    excluded_methods = ["calculate_ingredient_amounts"]

    def index(self):
        return self.template()

    def post(self):
        date_from = request.form["date_from"]
        date_to = request.form["date_to"]
        return redirect(
            url_for("DailyPlanExporterView:show", date_from=date_from, date_to=date_to)
        )

    def show(self, date_from, date_to):
        self.daily_plans = DailyPlan.load_by_date_range(date_from, date_to)
        # print(self.daily_plans)
        self.ingredients = DailyPlan.load_ingredient_amounts_for_daily_plans(
            [dp.id for dp in self.daily_plans]
        )

        return self.template()
