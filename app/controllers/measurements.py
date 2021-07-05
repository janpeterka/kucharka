from flask import request
from flask_security import login_required, roles_accepted

from app import turbo

from flask_classful import route

from app.models.measurements import Measurement

from app.helpers.helper_flask_view import HelperFlaskView


class MeasurementsView(HelperFlaskView):
    decorators = [login_required, roles_accepted("admin", "application_manager")]

    @login_required
    def before_request(self, name, id=None, *args, **kwargs):
        self.measurement = Measurement.load(id)
        self.validate_operation(id, self.measurement)

    def before_index(self):
        self.measurements = Measurement.load_all()

    def index(self):
        return self.template()

    @route("/edit/<id>", methods=["POST"])
    def edit(self, id):
        return turbo.stream(
            turbo.replace(
                self.template(template_name="_edit"), target=f"measurement-{id}"
            )
        )

    def put(self, id):
        self.measurement.name = request.form["measurement"]
        self.measurement.save()

        return turbo.stream(
            turbo.replace(
                self.template(template_name="_measurement"), target=f"measurement-{id}"
            )
        )

    def post(self):
        self.measurement = Measurement(name=request.form["measurement"])
        self.measurement.save()

        return turbo.stream(
            [
                turbo.append(
                    self.template(template_name="_measurement"), target="measurements"
                ),
                turbo.replace(
                    self.template(template_name="_add"),
                    target="measurement-create-form",
                ),
            ]
        )

    def delete(self, id):
        from app.helpers.turbo_flash import turbo_flash

        if self.measurement.is_used:
            return turbo_flash("Už je někde použité, nelze smazat!")

        self.measurement.delete()

        return turbo.stream(turbo.remove(target=f"measurement-{id}"))
