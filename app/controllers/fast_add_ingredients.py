from flask import request, redirect, url_for
from flask_classful import route
from flask_security import login_required

from app import turbo

from app.helpers.helper_flask_view import HelperFlaskView

from app.models import Recipe, Ingredient
from app.controllers import EditRecipeIngredientsView
from app.forms import IngredientsForm


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
                + EditRecipeIngredientsView().update_usable_ingredients(recipe)
            )
        else:
            return redirect(url_for("RecipesView:edit", id=recipe_id))
