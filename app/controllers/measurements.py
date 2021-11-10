from flask import request, redirect, url_for
from flask_security import login_required, roles_accepted

from app import turbo

from flask_classful import route

from app.models.measurements import Measurement

from app.helpers.turbo_flash import turbo_flash
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

    @route("/show_edit/<id>", methods=["POST"])
    def show_edit(self, id):
        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.after(
                        self.template(template_name="_edit"),
                        target=f"measurement-{self.measurement.id}",
                    ),
                    turbo.replace(
                        self.template(template_name="_measurement", editing=True),
                        target=f"measurement-{self.measurement.id}",
                    ),
                ]
            )
        else:
            return redirect(
                url_for("MeasurementsView:index", edit_id=self.measurement.id)
            )

    @route("measurements/hide_edit/<id>", methods=["POST"])
    def hide_edit(self, id):
        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.remove(
                        target=f"measurement-edit-{self.measurement.id}",
                    ),
                    turbo.replace(
                        self.template(template_name="_measurement"),
                        target=f"measurement-{self.measurement.id}",
                    ),
                ]
            )
        else:
            return redirect(url_for("MeasurementsView:index"))

    @route("measurements/post_edit/<id>", methods=["POST"])
    def post_edit(self, id):
        self.measurement.name = request.form["name"]
        self.measurement.description = request.form["description"]
        self.measurement.save()

        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.replace(
                        self.template(template_name="_measurement"),
                        target=f"measurement-{self.measurement.id}",
                    ),
                    turbo.remove(target=f"measurement-edit-{self.measurement.id}"),
                ]
            )
        else:
            return redirect(url_for("MeasurementsView:index"))

    def post(self):
        self.measurement = Measurement(name=request.form["measurement"])
        self.measurement.save()

        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.append(
                        self.template(template_name="_measurement"),
                        target="measurements",
                    ),
                    turbo.replace(
                        self.template(template_name="_add"),
                        target="measurement-create-form",
                    ),
                ]
            )
        else:
            return redirect(url_for("MeasurementsView:index"))

    def delete(self, id):
        if self.measurement.is_used:
            return turbo_flash("Už je někde použité, nelze smazat!")

        self.measurement.delete()

        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.remove(target=f"measurement-{id}"),
                    turbo.remove(target=f"measurement-edit-{id}"),
                ]
            )
        else:
            return redirect(url_for("MeasurementsView:index"))
