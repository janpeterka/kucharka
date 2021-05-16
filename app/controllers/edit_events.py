from flask import request

from flask_classful import route
from flask_security import login_required

from app import turbo

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.events import Event

from app.controllers.forms.events import EventsForm


class EditEventView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "events"

    def before_request(self, name, event_id):
        self.event = Event.load(event_id)
        self.validate_operation(event_id, self.event)

    @route("/edit/<event_id>", methods=["POST"])
    def edit(self, event_id):
        self.form = EventsForm(obj=self.event)
        return turbo.stream(
            turbo.replace(self.template(template_name="_edit"), target="event-info")
        )

    def put(self, event_id):
        self.form = EventsForm(request.form)
        if not self.form.validate_on_submit():
            return turbo.stream(
                turbo.replace(self.template(template_name="_edit"), target="event-info")
            )

        self.form.populate_obj(self.event)
        self.event.edit()

        return turbo.stream(
            turbo.replace(self.template(template_name="_info"), target="event-info")
        )
