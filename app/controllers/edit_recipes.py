from unidecode import unidecode

from flask import request, redirect, url_for, abort
from flask import render_template as template

from flask_classful import route

from flask_security import current_user

from app import turbo

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.ingredients import Ingredient
from app.models.recipes import Recipe


class EditRecipeView(HelperFlaskView):
    template_folder = "recipes/edit"

    def before_request(self, name, recipe_id=None, **kwargs):
        if recipe_id:
            self.recipe = Recipe.load(recipe_id)

        if recipe_id is not None:
            if self.recipe is None:
                abort(404)
            if not self.recipe.can_current_user_view:
                abort(403)

    @route("recipes/add_ingredient/<recipe_id>", methods=["POST"])
    def add_ingredient(self, recipe_id):
        self.ingredient = Ingredient.load(request.form["ingredient_option"])

        self.recipe.add_ingredient(self.ingredient)

        return turbo.stream(
            [
                turbo.append(
                    self.template(template_name="_edit_ingredient"),
                    target="ingredients",
                )
            ]
            + self.update_usable_ingredients(self.recipe)
        )

    @route("recipes/change_ingredient/<recipe_id>/<ingredient_id>", methods=["POST"])
    def change_ingredient_amount(self, recipe_id, ingredient_id):
        self.ingredient = Ingredient.load(ingredient_id)
        amount = request.form["amount"]

        amount_for_portion = float(amount) / float(self.recipe.portion_count)

        self.recipe.change_ingredient_amount(self.ingredient, amount_for_portion)
        self.ingredient.amount = amount_for_portion

        return turbo.stream(
            turbo.replace(
                self.template(template_name="_edit_ingredient"),
                target=f"ingredient-{self.ingredient.id}",
            )
        )

    @route("recipes/remove_ingredient/<recipe_id>/<ingredient_id>", methods=["POST"])
    def remove_ingredient(self, recipe_id, ingredient_id):
        ingredient = Ingredient.load(ingredient_id)

        self.recipe.remove_ingredient(ingredient)

        return turbo.stream(
            [turbo.remove(target=f"ingredient-{ingredient_id}")]
            + self.update_usable_ingredients(self.recipe)
        )

    @route("recipes/edit/description/<recipe_id>/", methods=["POST"])
    def post_description(self, recipe_id):
        description = request.form["description"]

        self.recipe.description = description
        self.recipe.edit()

        return redirect(url_for("RecipesView:show", id=self.recipe.id))

    @route("recipes/edit/refresh_usable_ingredients/<recipe_id>", methods=["POST"])
    def refresh_usable_ingredients(self, recipe_id):
        response = self.update_usable_ingredients(self.recipe)
        return turbo.stream(response)

    def update_usable_ingredients(self, recipe):
        unused_personal_ingredients = [
            i for i in current_user.ingredients if i not in recipe.ingredients
        ]

        unused_public_ingredients = [
            i for i in Ingredient.load_all_public() if i not in recipe.ingredients
        ]

        unused_personal_ingredients.sort(key=lambda x: unidecode(x.name.lower()))
        unused_public_ingredients.sort(key=lambda x: unidecode(x.name.lower()))

        return [
            turbo.replace(
                template(
                    "recipes/edit/_add_ingredient_form.html.j2",
                    personal_ingredients=unused_personal_ingredients,
                    public_ingredients=unused_public_ingredients,
                    recipe=recipe,
                ),
                target="add_ingredient_form",
            )
        ]
