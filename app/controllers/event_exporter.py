# from flask import redirect, url_for, request
from flask_security import login_required


from app.models.daily_plans import DailyPlan
from app.models.events import Event

from app.helpers.extended_flask_view import ExtendedFlaskView


class EventExporterView(ExtendedFlaskView):
    decorators = [login_required]
    template_folder = "event_exporter"

    def before_request(self, name, event_id=None, *args, **kwargs):
        super().before_request(name, id=event_id, *args, **kwargs)
        self.event = Event.load(event_id)
        self.daily_plans = self.event.daily_plans
        self.ingredients = DailyPlan.load_ingredient_amounts_for_daily_plans(
            [dp.id for dp in self.daily_plans], self.event.people_count
        )

    def show(self, event_id):
        return self.template()

    def show_shopping_list(self, event_id):
        return self.template(template_name="shopping_list")
