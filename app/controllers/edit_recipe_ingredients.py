from flask import request, redirect, url_for, flash
from flask import render_template as template

from flask_classful import route

from flask_security import current_user, login_required

from app import turbo

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.admin_view_mixin import AdminViewMixin

from app.models.ingredients import Ingredient
from app.models.recipes import Recipe


class EditRecipeIngredientView(HelperFlaskView, AdminViewMixin):
    decorators = [login_required]
    template_folder = "recipes/edit/ingredient"
    attribute_name = "ingredient"
    instance_name = "ingredient"
    excluded_methods = ["add_ingredient_to_recipe", "update_usable_ingredients"]

    @login_required
    def before_request(self, name, recipe_id, **kwargs):
        self.recipe = Recipe.load(recipe_id)
        self.validate_edit(self.recipe)

    @route("add_ingredient/<recipe_id>", methods=["POST"])
    def add_ingredient(self, recipe_id):
        self.ingredient = Ingredient.load(request.form["ingredient_option"])
        self.ingredient.is_measured = True

        self.recipe.add_ingredient(self.ingredient)

        return redirect(
            url_for("RecipeView:edit", id=self.recipe.id, editing_id=self.ingredient.id)
        )

    @route("update/<recipe_id>/<ingredient_id>", methods=["POST"])
    def update(self, recipe_id, ingredient_id):
        self.ingredient = Ingredient.load(ingredient_id)

        is_measured = "is-measured" in request.form

        amount = request.form["amount"]
        if not amount:
            amount = 0
        amount_for_portion = float(amount) / float(self.recipe.portion_count)

        comment = request.form["comment"]

        self.recipe.change_ingredient_amount(self.ingredient, amount_for_portion)
        self.recipe.change_ingredient_comment(self.ingredient, comment)
        self.recipe.change_ingredient_measured(self.ingredient, is_measured)

        return super().update()

    @route("delete/<recipe_id>/<ingredient_id>", methods=["POST"])
    def delete(self, recipe_id, ingredient_id):
        self.ingredient = Ingredient.load(ingredient_id)

        if not self.recipe.remove_ingredient(self.ingredient):
            flash("tato surovina u?? byla smaz??na.", "error")
            return redirect(url_for("RecipeView:edit", id=self.recipe.id))

        return redirect(url_for("RecipeView:edit", id=self.recipe.id))

    def update_usable_ingredients(self, recipe):
        unused_personal_ingredients = [
            i for i in current_user.personal_ingredients if i not in recipe.ingredients
        ]

        unused_public_ingredients = [
            i for i in Ingredient.load_all_public() if i not in recipe.ingredients
        ]

        return [
            turbo.replace(
                template(
                    "recipes/edit/_add_ingredient_form.html.j2",
                    personal_ingredients=unused_personal_ingredients,
                    public_ingredients=unused_public_ingredients,
                    recipe=recipe,
                ),
                target="add-ingredient-form",
            )
        ]
