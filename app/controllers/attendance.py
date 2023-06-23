from flask import request
from flask_security import login_required

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.form import create_form

from app.models import Event
from app.forms import AttendeeForm


class AttendanceView(HelperFlaskView):
    decorators = [login_required]

    def before_request(self, name, event_id, **kwargs):
        self.event = Event.load(event_id)
        self.validate_show(self.event)

    def index(self, event_id):
        self.changed_attendee_id = int(request.args.get("changed_attendee_id", -1))
        self.form = create_form(AttendeeForm)

        return self.template()

    def export(self, event_id):
        return self.template()
