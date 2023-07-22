from flask import redirect, request, flash

# from flask_classful import route
from flask_security import login_required

from app.helpers.helper_flask_view import HelperFlaskView

from app.models import Event
from app.forms import EventForm


class EventDuplicationView(HelperFlaskView):
    decorators = [login_required]

    def before_request(self, name, id):
        self.event = Event.load(id)

    def before_new(self, id):
        self.validate_show(self.event)

    def before_post(self, id):
        self.validate_show(self.event)

    def new(self, id):
        self.form = EventForm(obj=self.event)

        return self.template()

    def post(self, id):
        form = EventForm(request.form)

        event = self.event.duplicate(
            date_from=form.date_from.data,
            name=form.name.data,
            people_count=form.people_count.data,
        )

        flash("událost byla úspěšně zkopírována.", "success")

        return redirect(event.url)
