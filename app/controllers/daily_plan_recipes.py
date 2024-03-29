from flask import request, redirect, url_for, flash
from flask_classful import route
from flask_security import login_required

from app.helpers.helper_flask_view import HelperFlaskView

from app.models import DailyPlan, DailyPlanRecipe, Recipe
from app.services import DailyPlanManager


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
            self.daily_recipe = DailyPlanRecipe.load(daily_recipe_id)
            self.daily_plan = self.daily_recipe.daily_plan

        self.validate_edit(self.daily_plan)

    @route("daily_plans/add_recipe/<daily_plan_id>", methods=["POST"])
    def add_recipe(self, daily_plan_id):
        self.recipe = Recipe.load(int(request.form["recipe_id"]))

        if not self.recipe or not self.recipe.can_current_user_view:
            flash("recept nelze přidat")
            return redirect(url_for("DailyPlanView:show", id=self.daily_plan.id))

        self.daily_recipe = DailyPlanManager(self.daily_plan).add_recipe(self.recipe)

        return redirect(request.referrer)

    @route("daily_plans/add_shopping/<daily_plan_id>", methods=["POST"])
    def add_shopping(self, daily_plan_id):
        self.daily_recipe = DailyPlanManager(self.daily_plan).add_shopping()
        self.daily_recipe.meal_type = "nákup"
        self.daily_recipe.save()

        return redirect(url_for("DailyPlanView:show", id=self.daily_plan.id))

    @route("daily_plans/remove_recipe/<daily_recipe_id>", methods=["POST"])
    def remove_daily_recipe(self, daily_recipe_id):
        if not self.daily_recipe:
            flash("tento recept už je smazán.", "error")
            return redirect(url_for("DailyPlanView:show", id=self.daily_plan.id))

        if not DailyPlanManager(self.daily_plan).remove_daily_recipe(self.daily_recipe):
            flash("tento recept nemůžete odebrat.", "error")

        return redirect(url_for("DailyPlanView:show", id=self.daily_plan.id))

    @route("daily_plans/edit_recipe/<daily_recipe_id>", methods=["POST"])
    def update(self, daily_recipe_id):
        self.daily_recipe.portion_count = request.form.get(
            "portion-count", self.daily_recipe.portion_count
        )
        self.daily_recipe.meal_type = request.form.get(
            "meal-type", self.daily_recipe.meal_type
        )
        self.daily_recipe.edit()

        return redirect(
            url_for(
                "DailyPlanView:show",
                id=self.daily_plan.id,
                highlighted_recipe_id=self.daily_recipe.recipe.id,
            )
        )

    @route("change_daily_plan/<daily_recipe_id>", methods=["PATCH"])
    def change_daily_plan(self, daily_recipe_id):
        new_daily_plan = DailyPlan.load(int(request.form["daily_plan_id"]))
        position = int(request.form["position"])

        self.daily_recipe.daily_plan = new_daily_plan
        self.daily_recipe.edit()

        # this fills the gap created by removing recipe from old plan
        self.daily_plan.order_recipes()

        daily_recipes = update_position(
            new_daily_plan.daily_recipes,
            self.daily_recipe,
            position,
            from_other_list=True,
        )

        for daily_recipe in daily_recipes:
            daily_recipe.edit()

        return "Recipe moved", 200

    @route("sort/<daily_recipe_id>", methods=["PATCH"])
    def sort(self, daily_recipe_id):
        position = int(request.form["position"])

        daily_recipes = update_position(
            self.daily_plan.daily_recipes, self.daily_recipe, position
        )

        self.daily_plan.order_recipes()

        for daily_recipe in daily_recipes:
            daily_recipe.edit()

        return "Recipe position changed", 200


def update_position(elements, moved_element, new_position, from_other_list=False):
    current_position = moved_element.position

    if from_other_list:
        for element in elements:
            if element != moved_element and element.position >= new_position:
                element.position += 1

    elif not from_other_list and new_position < current_position:  # move up
        # Shift elements down to accommodate the moved element
        for element in elements:
            if (
                element != moved_element
                and element.position < current_position
                and element.position >= new_position
            ):
                element.position += 1
    elif not from_other_list and new_position > current_position:  # move down
        # Shift elements up to accommodate the moved element
        for element in elements:
            if (
                element != moved_element
                and element.position > current_position
                and element.position <= new_position
            ):
                element.position -= 1

    moved_element.position = new_position

    return elements
