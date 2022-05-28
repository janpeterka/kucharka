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
        self.validate_show(self.event)

        self.daily_plans = self.event.active_daily_plans
        self.split_recipes = self.event.daily_recipes_split_by_shopping

        self.ingredients = DailyPlan.load_ingredient_amounts_for_daily_plans(
            [dp.id for dp in self.daily_plans]
        )

    def show_list(self, event_id, show_type):
        return self._show_list(event_id, show_type)

    def show_list_pdf(self, event_id, show_type):
        string = self._show_list(event_id, show_type, is_print=True)
        return render_pdf(
            HTML(string=string),
            download_filename=f"{self.event.slugified_name}--nakupni-seznam.pdf",
            automatic_download=False,
        )

    def download_list_pdf(self, event_id, show_type):
        string = self._show_list(event_id, show_type, is_print=True)
        return render_pdf(
            HTML(string=string),
            download_filename=f"{self.event.slugified_name}--nakupni-seznam.pdf",
        )

    # Shopping list export

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

    def download_shopping_list_pdf(self, event_id):
        return redirect(
            url_for(
                "EventExporterView:download_list_pdf",
                event_id=event_id,
                show_type="table",
            )
        )

    # Ingredient list export

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

    def download_ingredient_list_pdf(self, event_id):
        return redirect(
            url_for(
                "EventExporterView:download_list_pdf",
                event_id=event_id,
                show_type="list",
            )
        )

    # Recipe list export

    def _recipe_list(self):
        return self.template(template_name="recipe_list")

    def show_recipe_list(self, event_id):
        return self._recipe_list()

    def show_recipe_list_pdf(self, event_id):
        return render_pdf(
            HTML(string=self._recipe_list()),
            download_filename=f"{self.event.slugified_name}--recepty.pdf",
            automatic_download=False,
        )

    def download_recipe_list_pdf(self, event_id):
        return render_pdf(
            HTML(string=self._recipe_list()),
            download_filename=f"{self.event.slugified_name}--recepty.pdf",
        )

    # Cookbook export
    def _cookbook(self, is_print=False):
        partial_templates = []
        for daily_plan in self.daily_plans:
            for daily_recipe in daily_plan.daily_recipes:
                recipe = daily_recipe.recipe
                if recipe.is_shopping:
                    continue
                recipe.reload()
                recipe.portion_count = daily_recipe.portion_count
                recipe_template = template(
                    "recipes/_show_simple.html.j2", recipe=recipe, print=is_print
                )
                partial_templates.append(recipe_template)

        self.recipes_html = "".join(partial_templates)

        return self.template(template_name="cookbook", print=is_print)

    def show_cookbook(self, event_id, **kwargs):
        return self._cookbook()

    def show_cookbook_pdf(self, event_id):
        return render_pdf(
            HTML(string=self._cookbook(is_print=True)),
            download_filename=f"{self.event.slugified_name}--kucharka.pdf",
            automatic_download=False,
        )

    def download_cookbook_pdf(self, event_id):
        return render_pdf(
            HTML(string=self._cookbook(is_print=True)),
            download_filename=f"{self.event.slugified_name}--kucharka.pdf",
        )

    # INTERNAL

    def _show_list(self, event_id, show_type, is_print=False):
        self._set_shoppings()

        self.lasting_ingredients_shopping.recipe_ingredient_amounts = (
            self._get_amounts_for_shopping(self.lasting_ingredients_shopping)
        )

        for shopping in self.shoppings:
            shopping.recipe_ingredient_amounts = self._get_amounts_for_shopping(
                shopping
            )

        return self.template(
            template_name="shopping_list", show_type=show_type, print=is_print
        )

    def _set_shoppings(self):
        # Nejdřív nákup před akcí - trvanlivé suroviny
        self.lasting_ingredients = [i for i in self.ingredients if i.is_lasting]
        self._sort_ingredients(self.lasting_ingredients)

        # Tohle je pro rozpadnutí
        self.lasting_ingredients_shopping = Shopping()
        self.lasting_ingredients_shopping.shopping_list = self.lasting_ingredients
        self.lasting_ingredients_shopping.daily_recipes = self.event.daily_recipes
        self.lasting_ingredients_shopping.grouped_shopping_list = (
            self._grouped_ingredients(self.lasting_ingredients)
        )

        # a pak pro každý mezinákupový období
        self.shoppings = []
        for section in self.split_recipes:
            # If first event day begins with Shopping
            if not section:
                continue
            section_ids = [dr.id for dr in section]
            shopping = Shopping()
            shopping.daily_recipes = list(section)
            shopping.date = section[0].daily_plan.date
            shopping.is_shopping = section[0].is_shopping

            shopping_list = DailyPlan.load_ingredient_amounts_for_daily_recipes(
                section_ids
            )

            shopping_list = [i for i in shopping_list if not i.is_lasting]
            self._sort_ingredients(shopping_list)

            shopping.shopping_list = shopping_list
            shopping.grouped_shopping_list = self._grouped_ingredients(shopping_list)
            self.shoppings.append(shopping)

    def _sort_ingredients(self, list_of_ingredients):
        list_of_ingredients.sort(
            key=lambda x: (
                getattr(x.category, "name", "ZZZ"),
                unidecode(x.name.lower()),
            )
        )

    def _grouped_ingredients(self, list_of_ingredients):
        unused_ingredient_categories = [i.category_name for i in list_of_ingredients]
        grouped_ingredients = {c: [] for c in unused_ingredient_categories}
        for i in list_of_ingredients:
            grouped_ingredients[i.category_name].append(i)

        return grouped_ingredients

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

                comment = ingredient.load_comment_by_recipe(event_recipe)

                recipe_ingredient_amounts[ingredient.id]["recipes"][event_recipe.id] = {
                    # "name": event_recipe.name,
                    "amount": amount,
                    "occurences": len(event_recipe.daily_plan_daily_recipes),
                    "comment": comment,
                }

        return recipe_ingredient_amounts
