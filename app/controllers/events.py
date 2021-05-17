from flask import redirect, url_for, request
from flask_classful import route
from flask_security import login_required

from app.helpers.form import save_form_to_session
from app.helpers.helper_flask_view import HelperFlaskView

from app.controllers.forms.events import EventsForm

from app.models.daily_plans import DailyPlan
from app.models.events import Event


class EventsView(HelperFlaskView):
    decorators = [login_required]

    def before_request(self, name, id=None):
        event_id = id
        self.event = Event.load(id)

        self.validate_operation(event_id, self.event)

    def before_new(self):
        self.form = EventsForm()

    def before_edit(self, id):
        self.form = EventsForm(obj=self.event)

    def index(self):
        return self.template()

    def new(self):
        return self.template()

    def edit(self, id):
        return self.template()

    def show(self, id):
        return self.template()

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
        self.event.delete()

        return redirect(url_for("EventsView:index"))

    def warnings(self, id):
        return self.template(template_name="_warnings")
