from flask_security import login_required
from flask_weasyprint import render_pdf, HTML

from app.helpers.helper_flask_view import HelperFlaskView

from app.models import Event
from app.services import EventTimetableConstructor


class EventTimetableExporterView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "event_exporter"

    def before_request(self, name, event_id=None, *args, **kwargs):
        self.event = Event.load(event_id)
        self.validate_show(self.event)

    def show(self, event_id):
        return self._recipe_list()

    def pdf(self, event_id):
        return render_pdf(
            HTML(string=self._recipe_list()),
            download_filename=f"{self.event.slugified_name}--recepty.pdf",
            automatic_download=False,
        )

    def download(self, event_id):
        return render_pdf(
            HTML(string=self._recipe_list()),
            download_filename=f"{self.event.slugified_name}--recepty.pdf",
        )

    def _recipe_list(self):
        self.timetable = EventTimetableConstructor(self.event)

        return self.template(template_name="recipe_list")
