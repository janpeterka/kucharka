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
        self.edit_id = int(request.args.get("edit_id", 0))

    def before_update(self, attendee_id):
        self.attendee = Attendee.load(attendee_id)

    def before_post(self, event_id):
        self.event = Event.load(event_id)

    def post(self, event_id):
        form = AttendeeForm(request.form)
        attendee = Attendee()
        attendee.fill(form)
        attendee.event_id = event_id
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
