from flask import request, redirect, url_for

from flask_classful import route
from flask_security import login_required, current_user

from app import turbo

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.turbo_flash import turbo_flash as flash

from app.models.events import Event
from app.models.users import User

from app.controllers.forms.events import EventsForm


class EditEventView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "events/edit"

    @login_required
    def before_request(self, name, event_id, **kwargs):
        self.event = Event.load(event_id)
        self.validate_operation(event_id, self.event)

    @route("/edit/<event_id>", methods=["POST"])
    def edit(self, event_id):
        if not self.event.can_current_user_edit:
            return redirect(url_for("EventsView:show", id=event_id))

        self.form = EventsForm(obj=self.event)

        if turbo.can_stream():
            return turbo.stream(
                turbo.replace(self.template(template_name="_info"), target="event-info")
            )
        else:
            return redirect(url_for("EventsView:edit", id=self.event.id))

    def post(self, event_id):
        if not self.event.can_current_user_edit:
            return redirect(url_for("EventsView:show", id=event_id))

        self.form = EventsForm(request.form)

        if not self.form.validate_on_submit():
            if turbo.can_stream():
                return turbo.stream(
                    turbo.replace(
                        self.template(template_name="_info"), target="event-info"
                    )
                )
            else:
                return redirect(url_for("EventsView:edit", id=self.event.id))

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
                        target=f"event-{event_id}-update-warning",
                    ),
                    to=self.event.other_user_ids,
                )
            except Exception as e:
                from sentry_sdk import capture_exception

                capture_exception(e)

        return redirect(url_for("EventsView:show", id=self.event.id))

    @route("/show-share-with-user/<event_id>", methods=["POST"])
    def show_share_with_user(self, event_id):
        return turbo.stream(
            turbo.after(
                self.template(template_name="_share_form"),
                target="event-more-options-button-row",
            )
        )

    @route("/share-with-user/<event_id>", methods=["POST"])
    def share_with_user(self, event_id):
        if not self.event.can_current_user_share:
            flash("Nemáte práva přidávat uživatele.", "warning")
            return redirect(url_for("EventsView:show", id=event_id))

        form = request.form

        user = User.load_by_attribute("email", form["email"])
        role = form["role"]

        if self.event.user_role(user):
            self.event.change_user_role(user, role)
            flash("Změnili jsme uživateli práva.", "success")
        elif user:
            self.event.add_user_role(user, role)
            flash("Pozvali jsme uživatele.", "success")
        else:
            flash("Tohoto uživatele nemůžeme přidat.", "error")

        return redirect(url_for("EventsView:show", id=event_id))

    @route("/remove-sharing/<event_id>/<user_id>", methods=["POST"])
    def remove_sharing(self, event_id, user_id):
        if not self.event.can_current_user_share:
            flash("Nemáte práva odebrat uživatele.", "warning")
            return redirect(url_for("EventsView:show", id=event_id))

        self.event.remove_user_role(User.load(user_id))
        flash("Odebrali jsme uživatele.", "success")

        return redirect(url_for("EventsView:show", id=event_id))


@turbo.user_id
def get_user_id():
    return current_user.id
