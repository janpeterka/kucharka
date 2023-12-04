from flask import redirect, url_for, request
from flask_security import login_required

from app.models.daily_plans import DailyPlan
from app.models.recipes import Recipe

from app.helpers.helper_flask_view import HelperFlaskView


class DailyPlanView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "daily_plans"

    @login_required
    def before_request(self, name, id, *args, **kwargs):
        self.daily_plan = DailyPlan.load(id)

        self.validate_show(self.daily_plan)

    def show(self, id):
        self.highlighted_recipe_id = int(request.args.get("highlighted_recipe_id", 0))
        self.editing_id = int(request.args.get("editing_id", 0))
        self.public_recipes = Recipe.load_all_public(exclude_mine=True)
        self.daily_recipes = self.daily_plan.daily_recipes
        self.daily_recipes.sort(key=lambda x: x.position)

        return self.template()

    def next(self, id):
        daily_plan = DailyPlan.load(id)

        return redirect(url_for("DailyPlanView:show", id=daily_plan.next.id))

    def previous(self, id):
        daily_plan = DailyPlan.load(id)

        return redirect(url_for("DailyPlanView:show", id=daily_plan.previous.id))
