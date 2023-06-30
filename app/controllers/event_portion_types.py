from flask import redirect, request
from flask_classful import route
from flask_security import login_required

from app.helpers.helper_flask_view import HelperFlaskView
from app.models import Event, EventPortionType, PortionType


class EventPortionTypeView(HelperFlaskView):
    decorators = [login_required]

    def before_request(self, name, event_id, portion_type_id, **kwargs):
        self.event = Event.load(event_id)
        self.validate_edit(self.event)

        self.portion_type = PortionType.load(portion_type_id)
        self.ept = EventPortionType.load_by_event_and_portion_type(
            self.event, self.portion_type
        )
        if not self.ept:
            self.ept = EventPortionType(
                event_id=self.event.id, portion_type_id=self.portion_type.id
            )
            self.ept.save()

    @route("add-portions/<event_id>/<portion_type_id>/<int:count>")
    def add_portions(self, event_id, portion_type_id, count):
        if self.event.people_count_without_portion_type < count:
            count = self.event.people_count_without_portion_type
        self.ept.count += int(count)
        self.ept.edit()

        return redirect(request.referrer)

    @route("substract-portions/<event_id>/<portion_type_id>/<int:count>")
    def substract_portions(self, event_id, portion_type_id, count):

        self.ept.count -= count
        self.ept.count = max(self.ept.count, 0)
        self.ept.edit()

        return redirect(request.referrer)
