from flask import request, redirect, url_for, flash
from flask_classful import route
from flask_security import login_required

from app.models.daily_plans import DailyPlan
from app.models.daily_plans_have_recipes import DailyPlanHasRecipe
from app.models.recipes import Recipe

from app.helpers.helper_flask_view import HelperFlaskView


class DailyPlanRecipeView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "daily_plans"
    route_prefix = "daily-plans"

    @login_required
    def before_request(
        self, name, daily_plan_id=None, daily_recipe_id=None, *args, **kwargs
    ):
        if daily_plan_id:
            self.daily_plan = DailyPlan.load(daily_plan_id)

        if daily_recipe_id:
            self.daily_recipe = DailyPlanHasRecipe.load(daily_recipe_id)
            self.daily_plan = self.daily_recipe.daily_plan

        self.validate_edit(self.daily_plan)

    @route("daily_plans/add_recipe/<daily_plan_id>", methods=["POST"])
    def add_recipe(self, daily_plan_id):
        self.recipe = Recipe.load(request.form["recipe_id"])

        if not self.recipe or not self.recipe.can_current_user_view:
            return redirect(url_for("DailyPlanView:show", id=self.daily_plan.id))

        self.daily_recipe = self.daily_plan.add_recipe(self.recipe)

        return redirect(url_for("DailyPlanView:show", id=self.daily_plan.id))

    @route("daily_plans/add_shopping/<daily_plan_id>", methods=["POST"])
    def add_shopping(self, daily_plan_id):
        self.daily_recipe = self.daily_plan.add_recipe(Recipe.load_shopping())
        self.daily_recipe.meal_type = "nákup"
        self.daily_recipe.save()

        return redirect(url_for("DailyPlanView:show", id=self.daily_plan.id))

    @route("daily_plans/remove_recipe/<daily_recipe_id>", methods=["POST"])
    def remove_daily_recipe(self, daily_recipe_id):
        if not self.daily_recipe:
            flash("tento recept už je smazán.", "error")
            return redirect(url_for("DailyPlanView:show", id=self.daily_plan.id))

        if not self.daily_plan.remove_daily_recipe(self.daily_recipe):
            flash("tento recept nemůžete odebrat.", "error")

        return redirect(url_for("DailyPlanView:show", id=self.daily_plan.id))

    @route("daily_plans/edit_recipe/<daily_recipe_id>", methods=["POST"])
    def edit_daily_recipe(self, daily_recipe_id):
        self.daily_recipe.portion_count = request.form.get(
            "portion-count", self.daily_recipe.portion_count
        )
        self.daily_recipe.meal_type = request.form.get(
            "meal-type", self.daily_recipe.meal_type
        )
        self.daily_recipe.save()

        return redirect(url_for("DailyPlanView:show", id=self.daily_plan.id))

    @route("sort/up/<daily_recipe_id>", methods=["POST"])
    def sort_up(self, daily_recipe_id):
        self.daily_recipe.change_order(order_type="up")

        return redirect(url_for("DailyPlanView:show", id=self.daily_plan.id))

    @route("sort/down/<daily_recipe_id>", methods=["POST"])
    def sort_down(self, daily_recipe_id):
        self.daily_recipe.change_order(order_type="down")

        return redirect(url_for("DailyPlanView:show", id=self.daily_plan.id))
