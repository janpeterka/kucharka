from flask import redirect, url_for
from flask import render_template as template
from flask_security import login_required
from flask_weasyprint import render_pdf, HTML

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.events import Event

from app.services import ShoppingListConstructor, EventTimetableConstructor


class EventExporterView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "event_exporter"

    def before_request(self, name, event_id=None, *args, **kwargs):
        self.event = Event.load(event_id)
        self.validate_show(self.event)

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
        self.timetable = EventTimetableConstructor(self.event)

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
        for daily_plan in self.event.active_daily_plans:
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
        shopping_list_constructor = ShoppingListConstructor(event=self.event)

        self.lasting_ingredients_shopping = (
            shopping_list_constructor.get_lasting_shopping()
        )
        self.shoppings = shopping_list_constructor.get_shoppings()

        self.lasting_ingredients_shopping.recipe_ingredient_amounts = (
            shopping_list_constructor.get_amounts_for_shopping(
                self.lasting_ingredients_shopping
            )
        )

        for shopping in self.shoppings:
            shopping.recipe_ingredient_amounts = (
                shopping_list_constructor.get_amounts_for_shopping(shopping)
            )

        return self.template(
            template_name="shopping_list", show_type=show_type, print=is_print
        )
