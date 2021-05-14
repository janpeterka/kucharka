from flask import request, redirect, url_for

from flask_classful import route
from flask_security import login_required

from app import turbo

from app.helpers.form import save_form_to_session
from app.helpers.helper_flask_view import HelperFlaskView

from app.models.events import Event

from app.controllers.forms.events import EventsForm


class EditEventView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "events"

    def before_request(self, name, event_id):
        self.event = Event.load(event_id)

    @route("events/show_edit/<event_id>", methods=["POST"])
    def show(self, event_id):
        self.form = EventsForm(obj=self.event)
        return turbo.stream(
            turbo.replace(self.template(template_name="_edit"), target="event-info")
        )

    @route("events/post_edit/<event_id>", methods=["POST"])
    def post(self, event_id):
        form = EventsForm(request.form)
        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("EditEventView:edit", event_id=self.event.id))

        form.populate_obj(self.event)
        self.event.edit()

        return turbo.stream(
            turbo.replace(self.template(template_name="_info"), target="event-info")
        )
