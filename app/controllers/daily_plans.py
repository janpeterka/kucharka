from flask import redirect, url_for
from flask_security import login_required

from app.models.daily_plans import DailyPlan
from app.models.recipes import Recipe

from app.helpers.helper_flask_view import HelperFlaskView


class DailyPlansView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "daily_plans"

    @login_required
    def before_request(self, name, daily_plan_id=None, *args, **kwargs):
        self.daily_plan = DailyPlan.load(daily_plan_id)
        self.validate_operation(daily_plan_id, self.daily_plan)

    def before_show(self, id):
        self.daily_plan = DailyPlan.load(id)
        self.public_recipes = Recipe.load_all_public(exclude_mine=True)
        self.daily_recipes = self.daily_plan.daily_recipes
        self.daily_recipes.sort(key=lambda x: x.order_index)

    def show(self, id):
        return self.template()

    def next(self, daily_plan_id):
        daily_plan = DailyPlan.load(daily_plan_id)
        return redirect(url_for("DailyPlansView:show", id=daily_plan.next.id))

    def previous(self, daily_plan_id):
        daily_plan = DailyPlan.load(daily_plan_id)
        return redirect(url_for("DailyPlansView:show", id=daily_plan.previous.id))
