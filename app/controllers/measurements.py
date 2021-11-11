from flask import request
from flask_security import login_required, roles_accepted

from flask_classful import route

from app.models.measurements import Measurement

from app.helpers.turbo_flash import turbo_flash
from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.admin_view_mixin import AdminViewMixin


class MeasurementsView(HelperFlaskView, AdminViewMixin):
    decorators = [login_required, roles_accepted("admin", "application_manager")]

    @login_required
    def before_request(self, name, id=None, *args, **kwargs):
        self.measurement = Measurement.load(id)
        self.validate_operation(id, self.measurement)

    def before_index(self):
        self.measurements = Measurement.load_all()

    def index(self):
        return self.template()

    @route("/show_edit/<id>", methods=["POST"])
    def show_edit(self, id):
        return super().show_edit()

    @route("measurements/hide_edit/<id>", methods=["POST"])
    def hide_edit(self, id):
        return super().hide_edit()

    @route("measurements/post_edit/<id>", methods=["POST"])
    def post_edit(self, id):
        self.measurement.name = request.form["name"]
        self.measurement.description = request.form["description"]
        self.measurement.save()

        return super().post_edit()

    def post(self):
        self.measurement = Measurement(name=request.form["measurement"])
        self.measurement.save()

        return super().post()

    def delete(self, id):
        if self.measurement.is_used:
            return turbo_flash("Už je někde použité, nelze smazat!")

        self.measurement.delete()

        return super().delete()
