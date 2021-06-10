from flask_security import login_required

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.daily_plans import DailyPlan
from app.models.events import Event
from app.models.shopping import Shopping


class EventExporterView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "event_exporter"

    def before_request(self, name, event_id=None, *args, **kwargs):
        self.event = Event.load(event_id)
        self.daily_plans = self.event.daily_plans
        self.split_recipes = self.event.daily_recipes_split_by_shopping

        self.ingredients = DailyPlan.load_ingredient_amounts_for_daily_plans(
            [dp.id for dp in self.daily_plans], self.event.people_count
        )

    def show(self, event_id):
        return self.template()

    def show_shopping_list(self, event_id):
        # Nejdřív nákup před akcí -. lasting
        self.lasting_ingredients = [i for i in self.ingredients if i.is_lasting]

        # a pak pro každý mezinákupový období
        self.shoppings = []
        for section in self.split_recipes:
            section_ids = [dr.id for dr in section]
            shopping = Shopping()
            shopping.date = section[0].daily_plan.date
            if section[0].is_shopping:
                shopping.is_shopping = True
            else:
                shopping.is_shopping = False

            shopping.shopping_list = (
                DailyPlan.load_ingredient_amounts_for_daily_recipes(
                    section_ids, self.event.people_count
                )
            )
            shopping.shopping_list = [
                i for i in shopping.shopping_list if not i.is_lasting
            ]
            self.shoppings.append(shopping)

        return self.template(template_name="shopping_list")

    def show_recipe_list(self, event_id):
        return self.template(template_name="recipe_list")

    def show_cookbook(self, event_id):
        return self.template(template_name="cookbook")

    def show_ingredient_list(self, event_id):
        used_recipes = self.event.recipes
        for ingredient in self.ingredients:
            ingredient.event_recipes = [
                r for r in ingredient.recipes if r in used_recipes
            ]
            for r in ingredient.event_recipes:
                r.occurences = len([p for p in r.daily_plans if p.event == self.event])

        recipe_ingredient_amounts = {}

        for ingredient in self.ingredients:
            recipe_ingredient_amounts[ingredient.id] = {
                "name": ingredient.name,
                "recipes": {},
            }
            for event_recipe in ingredient.event_recipes:
                amount = ingredient.load_amount_by_recipe(event_recipe) * float(
                    self.event.people_count
                )
                recipe_ingredient_amounts[ingredient.id]["recipes"][event_recipe.id] = {
                    "name": event_recipe.name,
                    "amount": amount,
                    "occurences": event_recipe.occurences,
                }

        return self.template(
            template_name="ingredient_list", amounts=recipe_ingredient_amounts
        )
