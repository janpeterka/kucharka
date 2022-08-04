from flask import request, redirect, url_for
from flask_security import login_required
from flask_classful import route

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.form import create_form

from app.models import Event, Attendee
from app.forms import AttendeeForm


class AttendanceView(HelperFlaskView):
    decorators = [login_required]

    def before_index(self, event_id):
        self.event = Event.load(event_id)
        self.validate_show(self.event)
        self.edit_id = int(request.args.get("edit_id", 0))

    def before_update(self, attendee_id):
        self.attendee = Attendee.load(attendee_id)
        self.validate_edit(self.attendee.event)

    def before_post(self, event_id, portion_type_id):
        self.event = Event.load(event_id)
        self.validate_edit(self.event)

    def before_delete(self, attendee_id):
        self.attendee = Attendee.load(attendee_id)
        self.validate_edit(self.attendee.event)

    def post(self, event_id, portion_type_id):
        form = AttendeeForm(request.form)
        attendee = Attendee(event_id=event_id, portion_type_id=portion_type_id)
        attendee.fill(form)
        attendee.save()

        return redirect(url_for("AttendanceView:index", event_id=event_id))

    def index(self, event_id):
        self.form = create_form(AttendeeForm)

        if self.edit_id > 0:
            self.edit_form = AttendeeForm(obj=Attendee.load(self.edit_id))

        return self.template()

    @route("update/<attendee_id>", methods=["POST"])
    def update(self, attendee_id):
        form = AttendeeForm(request.form)

        self.attendee.fill(form)
        self.attendee.edit()

        return redirect(
            url_for("AttendanceView:index", event_id=self.attendee.event.id)
        )

    @route("delete/<attendee_id>", methods=["POST"])
    def delete(self, attendee_id):
        self.attendee.delete()

        return redirect(request.referrer)
