from flask import request, redirect, url_for

from flask_classful import route
from flask_security import login_required

from app import turbo

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.ingredients import Ingredient
from app.models.ingredient_categories import IngredientCategory
from app.models.measurements import Measurement


def set_form(form, ingredient=None):
    measurements = Measurement.load_all()
    categories = IngredientCategory.load_all()

    form.set_all(measurements=measurements, categories=categories)

    if ingredient:
        if ingredient.measurement:
            form.measurement.data = ingredient.measurement.id
        if ingredient.category:
            form.category.data = ingredient.category.id


class PublicIngredientsView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "ingredients/public"

    def before_request(self, name, id=None, *args, **kwargs):
        self.ingredient = Ingredient.load(id)
        self.validate_operation(id, self.ingredient)

    def before_index(self):
        self.public_ingredients = Ingredient.load_all_public()

    def index(self):
        return self.template()

    @route("/ingredients/show_edit/<ingredient_id>", methods=["POST"])
    def edit(self, ingredient_id):
        self.ingredient = Ingredient.load(ingredient_id)

        self.measurements = Measurement.load_all()
        self.categories = IngredientCategory.load_all()

        # WIP - tohle teď index neumí
        return turbo.stream(
            turbo.replace(
                self.template(template_name="_edit"),
                target=f"ingredient-{ingredient_id}",
            )
        )

    @route("ingredients/edit/<id>", methods=["POST"])
    def post_edit(self, id):
        self.ingredient.category = IngredientCategory.load(request.form["category_id"])
        self.ingredient.measurement = Measurement.load(request.form["measurement_id"])

        self.ingredient.save()

        if turbo.can_stream():
            return turbo.stream(
                turbo.replace(
                    self.template(template_name="_ingredient"),
                    target=f"ingredient-{self.ingredient.id}",
                )
            )
        else:
            return redirect(url_for("PublicIngredientsView:index"))
