# import datetime

from flask import request
from flask_classful import route
from flask_security import login_required

from app import turbo

from app.models.daily_plans import DailyPlan
from app.models.daily_plans_have_recipes import DailyPlanHasRecipe
from app.models.recipes import Recipe

from app.helpers.helper_flask_view import HelperFlaskView


class DailyPlansView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "daily_plans"

    def before_request(self, name, id=None, daily_plan_id=None, *args, **kwargs):
        if not daily_plan_id:
            daily_plan_id = id

        self.daily_plan = DailyPlan.load(daily_plan_id)
        self.validate_operation(daily_plan_id, self.daily_plan)

    def before_show(self, id):
        self.public_recipes = Recipe.load_all_public(exclude_mine=True)

    def show(self, id):
        self.daily_plan = DailyPlan.load(id)
        self.daily_recipes = self.daily_plan.daily_recipes
        self.daily_recipes.sort(key=lambda x: x.order_index)

        return self.template()

    @route("daily_plans/remove_recipe/<daily_recipe_id>", methods=["POST"])
    def remove_daily_recipe(self, daily_recipe_id):
        daily_recipe = DailyPlanHasRecipe.load(daily_recipe_id)
        daily_plan = DailyPlan.load(daily_recipe.daily_plan.id)

        daily_plan.remove_daily_recipe_by_id(daily_recipe_id)

        return turbo.stream(turbo.remove(target=f"daily-recipe-{daily_recipe_id}"))

    @route("daily_plans/add_recipe/<daily_plan_id>", methods=["POST"])
    def add_recipe(self, daily_plan_id):
        recipe = Recipe.load(request.form["recipe_id"])

        self.daily_recipe = self.daily_plan.add_recipe(recipe)

        return turbo.stream(
            turbo.append(
                self.template(template_name="_recipe_row"), target="daily_recipes"
            )
        )

    # def sort_up(self, daily_recipe_id, date):
    #     self.daily_plan.change_order(daily_recipe_id, order_type="up")
    #     return redirect(url_for("DailyPlansView:show_by_date", date=date))

    # def sort_down(self, daily_recipe_id, date):
    #     self.daily_plan.change_order(daily_recipe_id, order_type="down")
    #     return redirect(url_for("DailyPlansView:show_by_date", date=date))

    # def next_day(self, id):
    #     pass

    # def previous_day(self, id):
    #     pass
