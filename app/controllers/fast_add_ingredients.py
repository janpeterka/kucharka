from flask import request, redirect, url_for

from flask_classful import route
from flask_security import login_required

from app import turbo

from app.helpers.helper_flask_view import HelperFlaskView

from app.models import Recipe, Ingredient

from app.controllers.edit_recipe_ingredients import EditRecipeIngredientsView

from app.controllers.forms.ingredients import IngredientsForm


class FastAddIngredientsView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "ingredients"

    @route("/show/<recipe_id>", methods=["POST"])
    def show(self, recipe_id):
        self.form = IngredientsForm()

        if turbo.can_stream():
            return turbo.stream(
                turbo.append(
                    self.template(
                        template_name="_new_simple", recipe=Recipe.load(recipe_id)
                    ),
                    target="add-ingredient",
                ),
            )
        else:
            return redirect(
                url_for("RecipesView:edit", id=recipe_id, show_fast_add=True)
            )

    @route("/hide/<recipe_id>", methods=["POST"])
    def hide(self, recipe_id):
        self.form = IngredientsForm()

        if turbo.can_stream():
            return turbo.stream(
                turbo.remove(
                    target="add-ingredient-simple",
                ),
            )
        else:
            return redirect(url_for("RecipesView:edit", id=recipe_id))

    @route("/post/<recipe_id>", methods=["POST"])
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
                + EditRecipeIngredientsView().add_ingredient_to_recipe(
                    recipe, ingredient
                )
                + EditRecipeIngredientsView().update_usable_ingredients(recipe)
            )
        else:
            return redirect(url_for("RecipesView:edit", id=recipe_id))
