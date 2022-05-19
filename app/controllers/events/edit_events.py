from flask import request, redirect, url_for

from flask_classful import route
from flask_security import login_required

from app import turbo

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.turbo_flash import turbo_flash as flash

from app.models.events import Event
from app.models.users import User


class EditEventView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "events/edit"

    @login_required
    def before_request(self, name, event_id, **kwargs):
        self.event = Event.load(event_id)
        self.validate_operation(event_id, self.event)

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
            return redirect(url_for("EventView:show", id=event_id))

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

        return redirect(url_for("EventView:show", id=event_id))

    @route("/remove-sharing/<event_id>/<user_id>", methods=["POST"])
    def remove_sharing(self, event_id, user_id):
        if not self.event.can_current_user_share:
            flash("Nemáte práva odebrat uživatele.", "warning")
            return redirect(url_for("EventView:show", id=event_id))

        self.event.remove_user_role(User.load(user_id))
        flash("Odebrali jsme uživatele.", "success")

        return redirect(url_for("EventView:show", id=event_id))
