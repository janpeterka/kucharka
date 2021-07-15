from flask import request, redirect, url_for
from flask_security import login_required, roles_accepted

# from app import turbo

from flask_classful import route

from app.models.conversions import Conversion
from app.models.ingredients import Ingredient

from app.helpers.helper_flask_view import HelperFlaskView


class ConversionsView(HelperFlaskView):
    decorators = [login_required, roles_accepted("admin", "application_manager")]

    def index(self):
        self.conversions = Conversion.load_all()
        self.ingredients = Ingredient.load_all()
        return self.template()

    @route("/add/<ingredient_id>", methods=["POST"])
    def add(self, ingredient_id):
        new_measurement_id = request.form["new_measurement_id"]
        amount_from = request.form["amount_from"]
        amount_to = request.form["amount_to"]

        conversion = Conversion(
            ingredient_id=ingredient_id,
            to_measurement_id=new_measurement_id,
            amount_from=amount_from,
            amount_to=amount_to,
        )
        conversion.save()

        if "next" in request.args:
            return redirect(request.args["next"])

        return redirect(url_for("ConversionsView:index"))