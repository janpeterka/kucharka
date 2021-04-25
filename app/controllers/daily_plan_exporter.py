from flask import redirect, url_for, request
from flask_security import login_required


from app.models.daily_plans import DailyPlan

from app.helpers.extended_flask_view import ExtendedFlaskView


class DailyPlanExporterView(ExtendedFlaskView):
    decorators = [login_required]

    def index(self):
        return self.template()

    def post(self):
        date_from = request.form["date_from"]
        date_to = request.form["date_to"]
        people_count = request.form["people_count"]
        return redirect(
            url_for(
                "DailyPlanExporterView:show",
                date_from=date_from,
                date_to=date_to,
                people_count=people_count,
            )
        )

    def show(self, date_from, date_to, people_count):
        self.people_count = people_count
        DailyPlan.create_if_not_exists(date_from)
        DailyPlan.create_if_not_exists(date_to)
        self.daily_plans = DailyPlan.load_by_date_range(date_from, date_to)
        self.ingredients = DailyPlan.load_ingredient_amounts_for_daily_plans(
            [dp.id for dp in self.daily_plans], people_count
        )

        return self.template()
