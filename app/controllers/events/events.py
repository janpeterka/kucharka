from flask import redirect, url_for, request, flash
from flask_classful import route
from flask_security import login_required

from app.helpers.form import save_form_to_session
from app.helpers.helper_flask_view import HelperFlaskView

from app.controllers.forms.events import EventsForm

from app.models.daily_plans import DailyPlan
from app.models.events import Event


class EventsView(HelperFlaskView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, id=None):
        event_id = id
        self.event = Event.load(event_id)

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

    @route("duplicate/<id>", methods=["POST"])
    def duplicate(self, id):
        new_event = self.event.duplicate()

        return redirect(url_for("EventsView:show", id=new_event.id))

    @route("events/toggle_archived/<id>", methods=["POST"])
    def toggle_archived(self, id):
        self.event.toggle_archived()

        return redirect(url_for("EventsView:show", id=self.event.id))

    @route("toggle_shared/<id>", methods=["POST"])
    def toggle_shared(self, id):
        toggled = self.event.toggle_shared()
        if toggled is True:
            flash("Akce byla zveřejněna.", "success")
        else:
            flash("Akce byla skryta před veřejností.", "success")
        return redirect(url_for("EventsView:show", id=self.event.id))

    @route("share_all_used_recipes/<id>", methods=["POST"])
    def share_all_used_recipes(self, id):
        self.event.share_all_used_recipes()
        flash("Všechny recepty byly zveřejněny.", "success")
        return redirect(url_for("EventsView:show", id=self.event.id))

    def warnings(self, id):
        return self.template(template_name="_warnings")
