from flask import redirect, url_for
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

    def _show_list(self, event_id, is_print=False):
        self._set_values()

        return self.template(template_name="shopping_list", print=is_print)

    def show_list(self, event_id):
        return self._show_list(event_id)

    def show_list_pdf(self, event_id):
        string = self._show_list(event_id, is_print=True)

        return render_pdf(
            HTML(string=string),
            download_filename=f"{self.event.slugified_name}--nakupni-seznam.pdf",
            automatic_download=False,
        )

    def download_list_pdf(self, event_id):
        string = self._show_list(event_id, is_print=True)
        return render_pdf(
            HTML(string=string),
            download_filename=f"{self.event.slugified_name}--nakupni-seznam.pdf",
        )

    # Shopping list export

    def show_table(self, event_id):
        return self._show_table(event_id)

    def show_table_pdf(self, event_id):
        string = self._show_table(event_id, is_print=True)

        return render_pdf(
            HTML(string=string),
            download_filename=f"{self.event.slugified_name}--nakupni-seznam.pdf",
            automatic_download=False,
        )

    def download_table_pdf(self, event_id):
        string = self._show_list(event_id, is_print=True)
        return render_pdf(
            HTML(string=string),
            download_filename=f"{self.event.slugified_name}--nakupni-seznam.pdf",
        )

    def _show_table(self, event_id, is_print=False):
        self._set_values()

        return self.template(template_name="shopping_table", print=is_print)

    def show_shopping_list(self, event_id):
        return redirect(url_for("EventExporterView:show_table", event_id=event_id))

    def show_shopping_list_pdf(self, event_id):
        return redirect(url_for("EventExporterView:show_table_pdf", event_id=event_id))

    def download_shopping_list_pdf(self, event_id):
        return redirect(
            url_for(
                "EventExporterView:download_table_pdf",
                event_id=event_id,
            )
        )

    # Ingredient list export

    def show_ingredient_list(self, event_id):
        return redirect(url_for("EventExporterView:show_list", event_id=event_id))

    def show_ingredient_list_pdf(self, event_id):
        return redirect(url_for("EventExporterView:show_list_pdf", event_id=event_id))

    def download_ingredient_list_pdf(self, event_id):
        return redirect(
            url_for(
                "EventExporterView:download_list_pdf",
                event_id=event_id,
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

    # INTERNAL

    def _set_values(self):
        self.shopping_list_constructor = ShoppingListConstructor(event=self.event)

        self.lasting_ingredients_shopping = (
            self.shopping_list_constructor.get_lasting_shopping()
        )
        self.shoppings = self.shopping_list_constructor.get_shoppings()

        self.lasting_ingredients_shopping.recipe_ingredient_amounts = (
            self.shopping_list_constructor.get_amounts_for_shopping(
                self.lasting_ingredients_shopping
            )
        )

        for shopping in self.shoppings:
            shopping.recipe_ingredient_amounts = (
                self.shopping_list_constructor.get_amounts_for_shopping(shopping)
            )
