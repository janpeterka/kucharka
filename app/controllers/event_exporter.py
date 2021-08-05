from unidecode import unidecode

from flask import redirect, url_for
from flask import render_template as template
from flask_security import login_required
from flask_weasyprint import render_pdf, HTML

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
            [dp.id for dp in self.daily_plans]
        )

    def show(self, event_id):
        return self.template()

    def show_list(self, event_id, show_type):
        return self._show_list(event_id, show_type)

    def show_list_pdf(self, event_id, show_type):
        return self._show_list(event_id, show_type, is_print=True)

    def _show_list(self, event_id, show_type, is_print=False):
        self._set_shoppings()

        self.lasting_ingredients_shopping.recipe_ingredient_amounts = (
            self._get_amounts_for_shopping(self.lasting_ingredients_shopping)
        )

        for shopping in self.shoppings:
            shopping.recipe_ingredient_amounts = self._get_amounts_for_shopping(
                shopping
            )

        if is_print:
            return render_pdf(
                HTML(
                    string=self.template(
                        template_name="shopping_list", show_type=show_type, print=True
                    )
                )
            )
        else:
            return self.template(template_name="shopping_list", show_type=show_type)

    def _set_shoppings(self):
        # Nejdřív nákup před akcí - trvanlivé suroviny
        self.lasting_ingredients = [i for i in self.ingredients if i.is_lasting]
        self._sort_ingredients(self.lasting_ingredients)

        # Tohle je pro rozpadnutí
        self.lasting_ingredients_shopping = Shopping()
        self.lasting_ingredients_shopping.shopping_list = self.lasting_ingredients
        self.lasting_ingredients_shopping.daily_recipes = self.event.daily_recipes

        # a pak pro každý mezinákupový období
        self.shoppings = []
        for section in self.split_recipes:
            # If first event day begins with Shopping
            if not section:
                continue
            section_ids = [dr.id for dr in section]
            shopping = Shopping()
            shopping.daily_recipes = [dr for dr in section]
            shopping.date = section[0].daily_plan.date
            shopping.is_shopping = True if section[0].is_shopping else False

            shopping_list = DailyPlan.load_ingredient_amounts_for_daily_recipes(
                section_ids
            )

            shopping_list = [i for i in shopping_list if not i.is_lasting]
            self._sort_ingredients(shopping_list)

            shopping.shopping_list = shopping_list
            self.shoppings.append(shopping)

    def _sort_ingredients(self, list_of_ingredients):
        list_of_ingredients.sort(
            key=lambda x: (
                getattr(x.category, "name", "ZZZ"),
                unidecode(x.name.lower()),
            )
        )

    def _get_amounts_for_shopping(self, shopping=None):
        used_recipes = [r.recipe for r in shopping.daily_recipes]
        recipe_ingredient_amounts = {}

        for ingredient in shopping.shopping_list:

            recipe_ingredient_amounts[ingredient.id] = {
                "name": ingredient.name,
                "recipes": {},
            }

            # Get list of recipes relevant for this shopping
            ingredient.event_recipes = [
                r for r in ingredient.recipes if r in used_recipes
            ]

            for event_recipe in ingredient.event_recipes:

                event_recipe.daily_plan_daily_recipes = [
                    dr
                    for dr in event_recipe.daily_plan_recipes
                    if dr in shopping.daily_recipes
                ]

                amount = sum(
                    (
                        ingredient.load_amount_by_recipe(event_recipe)
                        * float(dr.portion_count)
                    )
                    for dr in event_recipe.daily_plan_daily_recipes
                )

                recipe_ingredient_amounts[ingredient.id]["recipes"][event_recipe.id] = {
                    # "name": event_recipe.name,
                    "amount": amount,
                    "occurences": len(event_recipe.daily_plan_daily_recipes),
                }

        return recipe_ingredient_amounts

    def show_shopping_list(self, event_id):
        return redirect(
            url_for("EventExporterView:show_list", event_id=event_id, show_type="table")
        )

    def show_shopping_list_pdf(self, event_id):
        return redirect(
            url_for(
                "EventExporterView:show_list_pdf", event_id=event_id, show_type="table"
            )
        )

    def show_ingredient_list(self, event_id):
        return redirect(
            url_for("EventExporterView:show_list", event_id=event_id, show_type="list")
        )

    def show_ingredient_list_pdf(self, event_id):
        return redirect(
            url_for(
                "EventExporterView:show_list_pdf", event_id=event_id, show_type="list"
            )
        )

    def show_recipe_list(self, event_id):
        return self.template(template_name="recipe_list")

    def show_recipe_list_pdf(self, event_id):
        return render_pdf(
            HTML(string=self.template(template_name="recipe_list", print=True))
        )

    def show_recipe_list_visual(self, event_id):
        return self.template(template_name="recipe_list_visual")

    def show_recipe_list_visual_pdf(self, event_id):
        return render_pdf(
            HTML(string=self.template(template_name="recipe_list_visual", print=True))
        )

    def show_cookbook(self, event_id):
        partial_templates = []
        for daily_plan in self.event.daily_plans:
            for daily_recipe in daily_plan.daily_recipes:
                recipe = daily_recipe.recipe
                if recipe.is_shopping:
                    continue
                recipe.reload()
                recipe.portion_count = daily_recipe.portion_count
                recipe_template = template(
                    "recipes/_show_simple.html.j2", recipe=recipe
                )
                partial_templates.append(recipe_template)

        self.recipes_html = "".join(partial_templates)

        return self.template(template_name="cookbook")

    def show_cookbook_pdf(self, event_id):
        partial_templates = []
        for daily_plan in self.event.daily_plans:
            for daily_recipe in daily_plan.daily_recipes:
                recipe = daily_recipe.recipe
                if recipe.is_shopping:
                    continue
                recipe.reload()
                recipe.portion_count = daily_recipe.portion_count
                recipe_template = template(
                    "recipes/_show_simple.html.j2", recipe=recipe
                )
                partial_templates.append(recipe_template)

        self.recipes_html = "".join(partial_templates)
        return render_pdf(
            HTML(string=self.template(template_name="cookbook", print=True))
        )
