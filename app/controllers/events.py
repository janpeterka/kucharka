from flask import redirect, url_for, request
from flask_classful import route
from flask_security import login_required

from app import turbo

from app.helpers.form import save_form_to_session
from app.helpers.extended_flask_view import ExtendedFlaskView

from app.controllers.forms.events import EventsForm

from app.models.daily_plans import DailyPlan
from app.models.events import Event


class EventsView(ExtendedFlaskView):
    decorators = [login_required]
    template_folder = "events"

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

    @route("events/show_edit/<id>", methods=["POST"])
    def show_edit(self, id):
        self.form = EventsForm(obj=self.event)
        # Use this while edit:GET doesn't support stream (probably until WebSocket support)
        return turbo.stream(
            turbo.replace(self.template(template_name="_edit"), target="event-info")
        )

    @route("events/post_edit/<id>", methods=["POST"])
    def post_edit(self, id):
        super().post_edit(id)

        return turbo.stream(
            turbo.replace(self.template(template_name="_info"), target="event-info")
        )

    @route("events/delete/<id>", methods=["POST"])
    def delete(self, id):
        self.event.remove()
        return redirect(url_for("DashboardView:show"))

    def warnings(self, id):
        return self.template(template_name="_warnings")
