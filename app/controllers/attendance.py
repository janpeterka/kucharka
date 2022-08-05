from flask import request
from flask_security import login_required

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.form import create_form

from app.models import Event, Attendee
from app.forms import AttendeeForm


class AttendanceView(HelperFlaskView):
    decorators = [login_required]

    def before_request(self, name, event_id, **kwargs):
        self.event = Event.load(event_id)
        self.validate_show(self.event)

    def before_index(self, event_id):
        self.edit_id = int(request.args.get("edit_id", 0))

    def index(self, event_id):
        self.form = create_form(AttendeeForm)

        if self.edit_id > 0:
            self.edit_form = AttendeeForm(obj=Attendee.load(self.edit_id))

        return self.template()

    def export(self, event_id):
        return self.template()
