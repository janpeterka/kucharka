from flask import render_template as template
from flask_security import login_required
from flask_weasyprint import render_pdf, HTML

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.events import Event


class EventCookbookExporterView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "event_exporter"

    def before_request(self, name, event_id=None, *args, **kwargs):
        self.event = Event.load(event_id)
        self.validate_show(self.event)

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

    def show(self, event_id, **kwargs):
        return self._cookbook()

    def pdf(self, event_id):
        return render_pdf(
            HTML(string=self._cookbook(is_print=True)),
            download_filename=f"{self.event.slugified_name}--kucharka.pdf",
            automatic_download=False,
        )

    def download(self, event_id):
        return render_pdf(
            HTML(string=self._cookbook(is_print=True)),
            download_filename=f"{self.event.slugified_name}--kucharka.pdf",
        )
