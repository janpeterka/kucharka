from flask import request
from flask import render_template as template

from flask_classful import FlaskView, route

from flask_security import current_user

from app import turbo

# from app.handlers.data import DataHandler

# from app.models.diets import Diet
from app.models.ingredients import Ingredient
from app.models.recipes import Recipe
from app.models.recipe_categories import RecipeCategory


class BaseRecipesView(FlaskView):
    @route("/addIngredient/", methods=["POST"])
    def addIngredient(self):
        # new_recipe_created = False
        ingredient = Ingredient.load(request.form["ingredient_option"])
        if "recipe_id" in request.form and request.form["recipe_id"]:
            recipe = Recipe.load(request.form["recipe_id"])
        else:
            recipe = Recipe(name="---", created_by=current_user.id, is_draft=True)
            recipe.save()
            # new_recipe_created = True

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
            ),
            turbo.replace(
                template(
                    "recipes/new/_new_recipe_form.html.j2",
                    categories=RecipeCategory.load_all(),
                    recipe=recipe,
                ),
                target="save_recipe_form",
            ),
        ]
