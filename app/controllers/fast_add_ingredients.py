from flask import request, redirect, url_for
from flask_classful import route
from flask_security import login_required

from app import turbo

from app.helpers.helper_flask_view import HelperFlaskView

from app.models import Recipe, Ingredient
from app.forms import IngredientForm


class FastAddIngredientView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "ingredients"

    @route("/post/<recipe_id>", methods=["POST"])
    def post(self, recipe_id):
        from app.controllers import EditRecipeIngredientView

        recipe = Recipe.load(recipe_id)

        form = IngredientForm(request.form)

        ingredient = Ingredient()
        form.populate_obj(ingredient)
        ingredient.save()

        recipe.add_ingredient(ingredient)

        ingredient.set_additional_info(recipe)

        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.remove(target="add-ingredient-simple"),
                    turbo.prepend(
                        self.template(
                            template_name="recipes/edit/ingredient/_row.html.j2",
                            ingredient=ingredient,
                            recipe=recipe,
                        ),
                        target="ingredients",
                    ),
                    turbo.after(
                        self.template(
                            template_name="recipes/edit/ingredient/_edit.html.j2",
                            ingredient=ingredient,
                            recipe=recipe,
                        ),
                        target=f"ingredient-{ingredient.id}",
                    ),
                ]
                + EditRecipeIngredientView().update_usable_ingredients(recipe)
            )
        else:
            return redirect(url_for("RecipeView:edit", id=recipe_id))
