from flask import url_for, redirect, abort

from flask_classful import route
from flask_security import login_required, current_user

from app.modules.calendar import generate_ical, generate_ical_response

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.users import User


class UserCalendarView(HelperFlaskView):
    @login_required
    @route("create-cal", methods=["POST"])
    def create_calendar(self):
        current_user.set_calendar_hash()

        return redirect(url_for("UserView:show"))

    @route("ical/<calendar_hash>")
    def ical(self, calendar_hash):
        if not (user := User.load_by_calendar_hash(calendar_hash)):
            abort(404)

        return generate_ical(user.events)

    @route("ical/download/<calendar_hash>")
    def ical_download(self, calendar_hash):
        if not (user := User.load_by_calendar_hash(calendar_hash)):
            abort(404)

        return generate_ical_response(user.events)
