import json

from flask import jsonify, request, abort
from flask import render_template as template

from flask_classful import FlaskView, route

from app.handlers.data import DataHandler

# from app.models.diets import Diet
from app.models.ingredients import Ingredient


class BaseRecipesView(FlaskView):
    @route("/addIngredientWithAmount", methods=["POST"])
    def addIngredientWithAmount(self):
        ingredient = Ingredient.load(request.json["ingredient_id"])

        if not ingredient:
            abort(404)
        if not ingredient.can_current_user_add:
            abort(403)

        template_data = template(
            "recipes/_add_ingredient_with_amount.html.j2", ingredient=ingredient
        )
        result = {"ingredient": ingredient.json, "template_data": template_data}
        DataHandler.set_additional_request_data(
            item_type="add_ingredient_with_amount_AJAX", item_id=ingredient.id
        )

        return jsonify(result)
