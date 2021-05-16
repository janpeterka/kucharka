from unidecode import unidecode

from flask import request

from flask_classful import route
from flask_security import login_required

from app import turbo

from app.helpers.extended_flask_view import ExtendedFlaskView

from app.models.ingredients import Ingredient
from app.models.ingredient_categories import IngredientCategory
from app.models.recipes import Recipe
from app.models.measurements import Measurement

from app.controllers.edit_recipes import EditRecipeView

from app.controllers.forms.ingredients import IngredientsForm


def set_form(form, ingredient=None):
    measurements = Measurement.load_all()

    categories = IngredientCategory.load_all()
    categories.sort(key=lambda x: unidecode(x.name.lower()))

    form.set_all(measurements=measurements, categories=categories)

    if ingredient:
        if ingredient.measurement:
            form.measurement.data = ingredient.measurement.id
        if ingredient.category:
            form.category.data = ingredient.category.id


class FastAddIngredientsView(ExtendedFlaskView):
    decorators = [login_required]
    template_folder = "ingredients"

    def before_request(self, name, **kwargs):
        self.form = IngredientsForm()

    def before_new(self, **kwargs):
        set_form(self.form)

    def new(self, recipe_id):
        return turbo.stream(
            turbo.replace(
                self.template(
                    template_name="_new_simple", recipe=Recipe.load(recipe_id)
                ),
                target="add-ingredient-simple",
            )
        )

    @route("ingredients/fast/post/<recipe_id>", methods=["POST"])
    def post(self, recipe_id):
        form = IngredientsForm(request.form)
        set_form(form)

        ingredient = Ingredient()
        form.measurement.data = Measurement.load(form.measurement.data)
        form.populate_obj(ingredient)
        ingredient.save()

        recipe = Recipe.load(recipe_id)

        return turbo.stream(
            [turbo.remove(target="add-ingredient-simple")]
            + EditRecipeView().add_ingredient_to_recipe(recipe, ingredient)
            + EditRecipeView().update_usable_ingredients(recipe)
        )
