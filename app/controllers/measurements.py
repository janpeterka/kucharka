from flask import redirect, url_for, request
from flask_security import login_required
from flask import render_template as template

from app import turbo

from flask_classful import route

from app.models.measurements import Measurement

from app.helpers.auth import admin_required
from app.helpers.extended_flask_view import ExtendedFlaskView


class MeasurementsView(ExtendedFlaskView):
    decorators = [login_required, admin_required]

    @route("/", methods=["GET", "POST"])
    def index(self):
        self.measurements = Measurement.load_all()
        if request.method == "POST":
            measurement = Measurement(name=request.form["measurement"])
            measurement.save()
            self.measurements.append(measurement)
            if turbo.can_stream():
                return turbo.stream(
                    [
                        turbo.append(
                            template(
                                "measurements/_measurement.html.j2",
                                measurement=measurement,
                            ),
                            target="measurements",
                        ),
                        turbo.update(
                            template("measurements/_add.html.j2"), target="form"
                        ),
                    ]
                )
        return self.template()

    # def index(self):
    #     self.measurements = Measurement.load_all()
    #     return self.template()

    @route("/edit/<id>", methods=["GET", "POST"])
    def edit(self, id):
        self.measurements = Measurement.load_all()
        measurement = Measurement.load(id)
        if request.method == "POST":
            measurement.name = request.form["measurement"]
            measurement.save()
            return redirect(url_for("MeasurementsView:index"))

        return self.template(
            template_name="/measurements/index.html.j2", edit_id=measurement.id
        )
