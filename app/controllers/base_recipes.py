from flask import request
from flask import render_template as template

from flask_classful import FlaskView, route

from flask_security import current_user

from app import turbo

# from app.handlers.data import DataHandler

# from app.models.diets import Diet
from app.models.ingredients import Ingredient
from app.models.recipes import Recipe

# from app.models.recipe_categories import RecipeCategory


class BaseRecipesView(FlaskView):
    @route("recipes/edit/add_ingredient/<recipe_id>", methods=["POST"])
    def add_ingredient(self, recipe_id):
        ingredient = Ingredient.load(request.form["ingredient_option"])
        recipe = Recipe.load(recipe_id)

        recipe.add_ingredient(ingredient)

        return turbo.stream(
            [
                turbo.append(
                    template(
                        "recipes/_edit_ingredient.html.j2",
                        ingredient=ingredient,
                        recipe=recipe,
                    ),
                    target="ingredients",
                )
            ]
            + self.update_usable_ingredients(recipe)
        )

    @route("recipes/edit/refresh_usable_ingredients/<recipe_id>", methods=["POST"])
    def refresh_usable_ingredients(self, recipe_id):
        recipe = Recipe.load(recipe_id)
        response = self.update_usable_ingredients(recipe)
        return turbo.stream(response)

    def update_usable_ingredients(self, recipe):
        unused_ingredients = [
            i for i in current_user.ingredients if i not in recipe.ingredients
        ]

        unused_public_ingredients = [
            i for i in Ingredient.load_all_public() if i not in recipe.ingredients
        ]

        return [
            turbo.replace(
                template(
                    "recipes/new/_add_ingredient_form.html.j2",
                    personal_ingredients=unused_ingredients,
                    public_ingredients=unused_public_ingredients,
                    recipe=recipe,
                ),
                target="add_ingredient_form",
            )
        ]
