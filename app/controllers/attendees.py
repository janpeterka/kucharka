from app.helpers.helper_flask_view import HelperFlaskView

from app.models import Event, Attendee


class AttendeeView(HelperFlaskView):
    def before_request(self, name, event_id):
        self.event = Event.load(event_id)

    def new(self, event_id):
        return self.template()

    def post(self, event_id):
        attendee = Attendee()

    def show(self, event_id):
        return self.template()

    def edit(self, edit_id):
        return self.template()
