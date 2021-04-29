from flask import request
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
        # self.measurement = Measurement.load(id)
        if request.method == "POST":
            return turbo.stream(
                turbo.replace(
                    self.template(template_name="measurements/_edit.html.j2"),
                    target=f"measurement-{id}",
                )
            )

    @route("/edit/<id>", methods=["GET", "POST"])
    def edit(self, id):
        if request.method == "POST":
            self.measurement.name = request.form["measurement"]
            self.measurement.save()
            return turbo.stream(
                turbo.replace(
                    self.template(template_name="measurements/_measurement.html.j2"),
                    target=f"measurement-{id}",
                )
            )

        # WIP - move show_edit for "GET" when support for WebSocket

        else:
            return self.template(
                template_name="/measurements/index.html.j2", edit_id=id
            )

    @route("/create/", methods=["POST"])
    def create(self):
        self.measurement = Measurement(name=request.form["measurement"])
        self.measurement.save()

        return turbo.stream(
            [
                turbo.append(
                    self.template(template_name="measurements/_measurement.html.j2"),
                    target="measurements",
                ),
                turbo.update(
                    template("measurements/_add.html.j2"),
                    target="measurement-create-form",
                ),
            ]
        )

    @route("/delete/<id>", methods=["POST"])
    def delete(self, id):
        from app.helpers.turbo_flash import turbo_flash

        if self.measurement.is_used:
            return turbo_flash("Už je někde použité, nelze smazat!")

            # flash("Už je někde použité, nelze smazat!")
            # return turbo.stream(
            #     turbo.prepend(
            #         template(
            #             "measurements/_error.html.j2",
            #             message="Už je někde použité, nelze smazat!",
            #         ),
            #         target=f"measurement-{id}",
            #     )
            # )

        self.measurement.delete()
        return turbo.stream(turbo.remove(target=f"measurement-{id}"))
