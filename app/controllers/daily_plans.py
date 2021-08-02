# import datetime

from flask import request, redirect, url_for, flash
from flask_classful import route
from flask_security import login_required

# from flask_security import current_user


from app import turbo

from app.models.daily_plans import DailyPlan
from app.models.daily_plans_have_recipes import DailyPlanHasRecipe
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

    @route("daily_plans/add_recipe/<daily_plan_id>", methods=["POST"])
    def add_recipe(self, daily_plan_id):
        recipe = Recipe.load(request.form["recipe_id"])

        self.daily_recipe = self.daily_plan.add_recipe(recipe)

        if turbo.can_stream():
            return turbo.stream(
                turbo.append(
                    self.template(template_name="_recipe_row"), target="daily_recipes"
                )
            )
        else:
            return redirect(url_for("DailyPlansView:show", id=self.daily_plan.id))

    @route("daily_plans/add_shopping/<daily_plan_id>", methods=["POST"])
    def add_shopping(self, daily_plan_id):
        recipe = Recipe.load_by_name("Nákup")
        self.daily_recipe = self.daily_plan.add_recipe(recipe)
        self.daily_recipe.meal_type = "nákup"
        self.daily_recipe.save()

        if turbo.can_stream():
            return turbo.stream(
                turbo.append(
                    self.template(template_name="_recipe_row"), target="daily_recipes"
                )
            )
        else:
            return redirect(url_for("DailyPlansView:show", id=self.daily_plan.id))

    @route(
        "daily_plans/remove_recipe/<daily_recipe_id>/<daily_plan_id>", methods=["POST"]
    )
    def remove_daily_recipe(self, daily_recipe_id, daily_plan_id):
        daily_recipe = DailyPlanHasRecipe.load(daily_recipe_id)
        if not daily_recipe:
            flash("Tento recept už je smazán.", "error")
            return redirect(url_for("DailyPlansView:show", id=daily_plan_id))

        daily_plan = daily_recipe.daily_plan

        if daily_plan.remove_daily_recipe(daily_recipe):

            if turbo.can_stream():
                return turbo.stream(
                    turbo.remove(target=f"daily-recipe-{daily_recipe_id}")
                )
            else:
                return redirect(url_for("DailyPlansView:show", id=daily_plan.id))
        else:
            flash("Tento recept nemůžete odebrat.", "error")
            return redirect(url_for("DailyPlansView:show", id=daily_plan.id))

    @route("change_meal_type/<daily_recipe_id>", methods=["POST"])
    def change_meal_type(self, daily_recipe_id):
        self.daily_recipe = DailyPlanHasRecipe.load(daily_recipe_id)
        self.daily_recipe.meal_type = request.form["meal-type"]
        self.daily_recipe.save()

        if turbo.can_stream():
            return turbo.stream(
                turbo.replace(
                    self.template(template_name="_recipe_row"),
                    target=f"daily-recipe-{self.daily_recipe.id}",
                )
            )
        else:
            return redirect(url_for("DailyPlansView:show", id=self.daily_plan.id))

    @route("change_portion_count/<daily_recipe_id>", methods=["POST"])
    def change_portion_count(self, daily_recipe_id):
        self.daily_recipe = DailyPlanHasRecipe.load(daily_recipe_id)
        self.daily_recipe.portion_count = request.form["portion-count"]
        self.daily_recipe.save()

        if turbo.can_stream():
            return turbo.stream(
                turbo.replace(
                    self.template(template_name="_recipe_row"),
                    target=f"daily-recipe-{self.daily_recipe.id}",
                )
            )
        else:
            return redirect(url_for("DailyPlansView:show", id=self.daily_plan.id))

    @route("sort/up/<daily_recipe_id>", methods=["POST"])
    def sort_up(self, daily_recipe_id):
        self.daily_recipe = DailyPlanHasRecipe.load(daily_recipe_id)
        self.daily_recipe.change_order(order_type="up")
        return redirect(
            url_for("DailyPlansView:show", id=self.daily_recipe.daily_plan.id)
        )

    @route("sort/down/<daily_recipe_id>", methods=["POST"])
    def sort_down(self, daily_recipe_id):
        self.daily_recipe = DailyPlanHasRecipe.load(daily_recipe_id)
        self.daily_recipe.change_order(order_type="down")
        return redirect(
            url_for("DailyPlansView:show", id=self.daily_recipe.daily_plan.id)
        )

    def next(self, daily_plan_id):
        daily_plan = DailyPlan.load(daily_plan_id)
        return redirect(url_for("DailyPlansView:show", id=daily_plan.next.id))

    def previous(self, daily_plan_id):
        daily_plan = DailyPlan.load(daily_plan_id)
        return redirect(url_for("DailyPlansView:show", id=daily_plan.previous.id))
