from flask import request, redirect, url_for

from flask_classful import route
from flask_security import login_required

from app import turbo

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.ingredients import Ingredient
from app.models.recipes import Recipe

from app.controllers.edit_recipes import EditRecipeView

from app.controllers.forms.ingredients import IngredientsForm


class FastAddIngredientsView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "ingredients"

    def new(self, recipe_id):
        self.form = IngredientsForm()
        # TODO: make it work without turbo (80)
        return turbo.stream(
            turbo.replace(
                self.template(
                    template_name="_new_simple", recipe=Recipe.load(recipe_id)
                ),
                target="add-ingredient-form",
            )
        )

    @route("ingredients/fast/post/<recipe_id>", methods=["POST"])
    def post(self, recipe_id):
        recipe = Recipe.load(recipe_id)

        form = IngredientsForm(request.form)

        ingredient = Ingredient()
        form.populate_obj(ingredient)
        ingredient.save()

        recipe.add_ingredient(ingredient)

        ingredient.set_additional_info(recipe)

        if turbo.can_stream():
            return turbo.stream(
                [turbo.remove(target="add-ingredient-simple")]
                + EditRecipeView().add_ingredient_to_recipe(recipe, ingredient)
                + EditRecipeView().update_usable_ingredients(recipe)
            )
        else:
            return redirect(url_for("RecipesView:edit", id=recipe_id))
