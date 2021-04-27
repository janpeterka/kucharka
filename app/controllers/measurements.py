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

    def before_request(self, name, id=None, *args, **kwargs):
        super().before_request(name, id, *args, **kwargs)
        self.measurements = Measurement.load_all()

    @route("/show_edit/<id>", methods=["POST"])
    def show_edit(self, id):
        # Use this while edit:GET doesn't support stream (probably until WebSocket support)
        self.measurement = Measurement.load(id)
        if request.method == "POST":
            if turbo.can_stream():
                return turbo.stream(
                    turbo.replace(
                        self.template(template="measurements/_edit.html.j2"),
                        target=f"measurement-{id}",
                    )
                )
            else:
                return self.template(template="/measurements/index.html.j2", edit_id=id)

    @route("/edit/<id>", methods=["GET", "POST"])
    def edit(self, id):
        self.measurement = Measurement.load(id)
        if request.method == "POST":
            self.measurement.name = request.form["measurement"]
            self.measurement.save()
            if turbo.can_stream():
                return turbo.stream(
                    turbo.replace(
                        self.template(template="measurements/_measurement.html.j2"),
                        target=f"measurement-{id}",
                    )
                )
            else:
                return redirect(url_for("MeasurementsView:index"))

        # elif request.method == "GET":
        #     # WIP - currently cannot stream here, so it's always `else`
        #     if turbo.can_stream():
        #         print("can_stream")
        #         return turbo.stream(
        #             turbo.replace(
        #                 template("measurements/_edit.html.j2", measurement=measurement),
        #                 target=f"measurement-{measurement.id}",
        #             )
        #         )
        else:
            return self.template(template="/measurements/index.html.j2", edit_id=id)

    @route("/create", methods=["POST"])
    def create(self):
        self.measurement = Measurement(name=request.form["measurement"])
        self.measurement.save()

        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.append(
                        self.template(template="measurements/_measurement.html.j2"),
                        target="measurements",
                    ),
                    turbo.update(
                        template("measurements/_add.html.j2"),
                        target="measurement-create-form",
                    ),
                ]
            )
        else:
            self.measurements.append(self.measurement)
            return self.template()
