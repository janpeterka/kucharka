from flask import request, redirect, url_for
from flask_security import login_required
from flask_classful import route

from app.helpers.helper_flask_view import HelperFlaskView

from app.models import Event, Attendee
from app.forms import AttendeeForm


class AttendeeView(HelperFlaskView):
    decorators = [login_required]

    def before_request(self, name, id=None, **kwargs):
        self.attendee = Attendee.load(id)
        if id:
            self.validate_show(self.attendee.event)

    def before_update(self, id):
        self.validate_edit(self.attendee.event)

    def before_delete(self, id):
        self.validate_edit(self.attendee.event)

    def before_post(self, event_id, portion_type_id):
        self.event = Event.load(event_id)
        self.validate_edit(self.event)

    def post(self, event_id, portion_type_id):
        form = AttendeeForm(request.form)
        attendee = Attendee(event_id=event_id, portion_type_id=portion_type_id)
        attendee.fill(form)
        attendee.save()

        return redirect(url_for("AttendanceView:index", event_id=event_id))

    @route("delete/<id>", methods=["POST"])
    def delete(self, id):
        self.attendee.delete()

        return redirect(request.referrer)

    @route("update/<id>", methods=["POST"])
    def update(self, id):
        form = AttendeeForm(request.form)

        self.attendee.fill(form)
        self.attendee.edit()

        return redirect(
            url_for("AttendanceView:index", event_id=self.attendee.event.id)
        )
