from flask import redirect, url_for, request
from flask_classful import route
from flask_security import login_required

from app.helpers.form import save_form_to_session
from app.helpers.extended_flask_view import ExtendedFlaskView

from app.controllers.forms.events import EventsForm

from app.models.daily_plans import DailyPlan
from app.models.events import Event


class EventsView(ExtendedFlaskView):
    decorators = [login_required]
    template_folder = "events"

    def before_request(self, name, id):
        self.event = Event.load(id)

    def post(self):
        form = EventsForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("EventsView:new"))

        event = Event()
        form.populate_obj(event)
        event.save()

        for day in event.days:
            day_plan = DailyPlan(date=day, event=event)
            day_plan.save()

        return redirect(url_for("EventsView:show", id=event.id))

    @route("events/delete/<id>", methods=["POST"])
    def delete(self, id):
        self.event.remove()
        return redirect(url_for("DashboardView:show"))

    def warnings(self, id):
        return self.template(template_name="_warnings")
