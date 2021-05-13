# from flask import redirect, url_for, request
from flask_security import login_required


from app.models.daily_plans import DailyPlan
from app.models.events import Event

# from app.models.ingredients import Ingredient

from app.helpers.extended_flask_view import ExtendedFlaskView


class EventExporterView(ExtendedFlaskView):
    decorators = [login_required]
    template_folder = "event_exporter"

    def before_request(self, name, event_id=None, *args, **kwargs):
        # super().before_request(name, id=event_id, *args, **kwargs)
        self.event = Event.load(event_id)
        self.daily_plans = self.event.daily_plans
        self.ingredients = DailyPlan.load_ingredient_amounts_for_daily_plans(
            [dp.id for dp in self.daily_plans], self.event.people_count
        )

    def show(self, event_id):
        return self.template()

    def show_shopping_list(self, event_id):
        return self.template(template_name="shopping_list")

    def show_recipe_list(self, event_id):
        return self.template(template_name="recipe_list")

    def show_cookbook(self, event_id):
        return self.template(template_name="cookbook")

    def show_ingredient_list(self, event_id):
        usable_recipes = self.event.recipes
        for ingredient in self.ingredients:
            ingredient.event_recipes = [
                i for i in ingredient.recipes if i in usable_recipes
            ]

        recipe_ingredient_amounts = {}

        for ingredient in self.ingredients:
            recipe_ingredient_amounts[ingredient.id] = {
                "name": ingredient.name,
                "recipes": {},
            }
            for event_recipe in ingredient.event_recipes:
                amount = ingredient.load_amount_by_recipe_id(event_recipe.id) * float(
                    self.event.people_count
                )
                recipe_ingredient_amounts[ingredient.id]["recipes"][event_recipe.id] = {
                    "name": event_recipe.name,
                    "amount": amount,
                }

        return self.template(
            template_name="ingredient_list", amounts=recipe_ingredient_amounts
        )
