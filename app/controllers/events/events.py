from flask import redirect, url_for, request, flash
from flask_classful import route
from flask_security import login_required

from app import turbo

from app.helpers.form import save_form_to_session
from app.helpers.helper_flask_view import HelperFlaskView

from app.models import DailyPlan, Event
from app.forms import EventForm


class EventView(HelperFlaskView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, id=None):
        event_id = id
        self.event = Event.load(event_id)

        self.validate_operation(event_id, self.event)

    def before_new(self):
        self.form = EventForm()

    def before_edit(self, id):
        self.validate_edit(self.event)

    def before_update(self, id):
        self.validate_edit(self.event)

    def index(self):
        return self.template()

    def new(self):
        return self.template()

    def edit(self, id):
        self.form = EventForm(obj=self.event)

        return self.template()

    def show(self, id):
        return self.template()

    def post(self):
        form = EventForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("EventView:new"))

        event = Event()
        form.populate_obj(event)
        event.save()

        for day in event.days:
            day_plan = DailyPlan(date=day, event=event)
            day_plan.save()

        return redirect(url_for("EventView:show", id=event.id))

    @route("update/<id>", methods=["POST"])
    def update(self, id):
        self.form = EventForm(request.form)

        old_people_count = None
        new_people_count = None
        if self.event.people_count != self.form.people_count.data:
            old_people_count = self.event.people_count
            new_people_count = int(self.form.people_count.data)

        self.form.populate_obj(self.event)

        self.event.edit()

        if old_people_count and new_people_count:
            for daily_plan in self.event.daily_plans:
                for daily_recipe in daily_plan.daily_recipes:
                    if daily_recipe.portion_count == old_people_count:
                        daily_recipe.portion_count = new_people_count
                        daily_recipe.edit()

        # TODO: do this only if date changed (70)
        # self.event.delete_old_daily_plans()
        self.event.add_new_daily_plans()

        if turbo.can_push():
            try:
                turbo.push(
                    turbo.update(
                        self.template(template_name="_update_warning"),
                        target=f"event-{id}-update-warning",
                    ),
                    to=self.event.other_user_ids,
                )
            except Exception as e:
                from sentry_sdk import capture_exception

                capture_exception(e)

        return redirect(url_for("EventView:show", id=self.event.id))

    @route("events/delete/<id>", methods=["POST"])
    def delete(self, id):
        self.event.delete()

        return redirect(url_for("EventView:index"))

    @route("duplicate/<id>", methods=["POST"])
    def duplicate(self, id):
        new_event = self.event.duplicate()

        return redirect(url_for("EventView:show", id=new_event.id))

    @route("events/toggle_archived/<id>", methods=["POST"])
    def toggle_archived(self, id):
        self.event.toggle_archived()

        return redirect(url_for("EventView:show", id=self.event.id))

    @route("toggle_shared/<id>", methods=["POST"])
    def toggle_shared(self, id):
        toggled = self.event.toggle_shared()
        if toggled is True:
            flash("Akce byla zveřejněna.", "success")
        else:
            flash("Akce byla skryta před veřejností.", "success")
        return redirect(url_for("EventView:show", id=self.event.id))

    @route("share_all_used_recipes/<id>", methods=["POST"])
    def share_all_used_recipes(self, id):
        self.event.share_all_used_recipes()
        flash("Všechny recepty byly zveřejněny.", "success")
        return redirect(url_for("EventView:show", id=self.event.id))

    def warnings(self, id):
        return self.template(template_name="_warnings")
