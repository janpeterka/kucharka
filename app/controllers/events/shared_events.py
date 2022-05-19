from flask import redirect, url_for
from flask_security import current_user

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.events import Event


class SharedEventView(HelperFlaskView):
    template_folder = "events"

    def before_request(self, name, hash_value):
        from app.helpers.general import unobscure

        event_id = unobscure(hash_value)
        self.event = Event.load(event_id)

        self.validate_show(self.event)

        if current_user in self.event.connected_users:
            return redirect(url_for("EventView:show", id=event_id))

    def show(self, hash_value):
        return self.template()
