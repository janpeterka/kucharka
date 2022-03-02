from app.helpers.helper_flask_view import HelperFlaskView

from app.models.events import Event


class SharedEventsView(HelperFlaskView):
    template_folder = "events"

    def before_request(self, name, hash_value=None):
        from app.helpers.general import unobscure

        event_id = unobscure(hash_value)
        self.event = Event.load(event_id)

        self.validate_operation(event_id, self.event)

    def show(self, hash_value):
        return self.template()
