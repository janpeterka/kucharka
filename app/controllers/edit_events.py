from flask import request, redirect, url_for

from flask_classful import route
from flask_security import login_required

from app import turbo

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.events import Event

from app.controllers.forms.events import EventsForm


class EditEventView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "events/edit"

    def before_request(self, name, event_id):
        self.event = Event.load(event_id)
        self.validate_operation(event_id, self.event)

    @route("/edit/<event_id>", methods=["POST"])
    def edit(self, event_id):
        self.form = EventsForm(obj=self.event)
        if turbo.can_stream():
            return turbo.stream(
                turbo.replace(self.template(template_name="_info"), target="event-info")
            )
        else:
            return redirect(url_for("EventsView:edit", id=self.event.id))

    def post(self, event_id):
        self.form = EventsForm(request.form)
        if not self.form.validate_on_submit():
            return turbo.stream(
                turbo.replace(self.template(template_name="_info"), target="event-info")
            )

        self.form.populate_obj(self.event)
        self.event.edit()

        if turbo.can_stream():
            return turbo.stream(
                turbo.replace(
                    self.template(template_name="events/_info.html.j2"),
                    target="event-info",
                )
            )
        else:
            return redirect(url_for("EventsView:show", id=self.event.id))
