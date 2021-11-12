from flask import request, redirect, url_for, flash
from flask import render_template as template

from flask_classful import route

from flask_security import current_user, login_required

from app import turbo

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.admin_view_mixin import AdminViewMixin

from app.models.ingredients import Ingredient
from app.models.recipes import Recipe


class EditRecipeIngredientsView(HelperFlaskView, AdminViewMixin):
    decorators = [login_required]
    template_folder = "recipes/edit/ingredient"
    attribute_name = "ingredient"
    instance_name = "ingredient"
    excluded_methods = ["add_ingredient_to_recipe", "update_usable_ingredients"]

    @login_required
    def before_request(self, name, recipe_id, **kwargs):
        self.recipe = Recipe.load(recipe_id)
        self.validate_operation(recipe_id, self.recipe)

    @route("show_edit/<recipe_id>/<ingredient_id>", methods=["POST"])
    def show_ingredient_edit(self, recipe_id, ingredient_id):
        self.ingredient = Ingredient.load(ingredient_id)
        return super().show_edit()

    @route("add_ingredient/<recipe_id>", methods=["POST"])
    def add_ingredient(self, recipe_id):
        self.ingredient = Ingredient.load(request.form["ingredient_option"])
        self.ingredient.is_measured = True

        self.recipe.add_ingredient(self.ingredient)

        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.prepend(
                        self.template(template_name="_row"),
                        target="ingredients",
                    )
                ]
                + self.update_usable_ingredients(self.recipe)
            )
        else:
            return redirect(url_for("RecipesView:edit", id=self.recipe.id))

    def add_ingredient_to_recipe(self, recipe, ingredient):
        recipe.add_ingredient(ingredient)
        return [
            turbo.append(
                self.template(
                    template_name="_row",
                    ingredient=ingredient,
                    recipe=recipe,
                ),
                target="ingredients",
            )
        ]

    @route("change_amount/<recipe_id>/<ingredient_id>", methods=["POST"])
    def change_ingredient_amount(self, recipe_id, ingredient_id):
        self.ingredient = Ingredient.load(ingredient_id)
        amount = request.form["amount"]
        if not amount:
            amount = 0

        amount_for_portion = float(amount) / float(self.recipe.portion_count)

        self.recipe.change_ingredient_amount(self.ingredient, amount_for_portion)
        self.ingredient.amount = amount_for_portion

        if turbo.can_stream():
            return turbo.stream(
                turbo.replace(
                    self.template(template_name="_row"),
                    target=f"ingredient-{self.ingredient.id}",
                )
            )
        else:
            return redirect(url_for("RecipesView:edit", id=self.recipe.id))

    @route("change_comment/<recipe_id>/<ingredient_id>", methods=["POST"])
    def change_ingredient_comment(self, recipe_id, ingredient_id):
        self.ingredient = Ingredient.load(ingredient_id)
        comment = request.form["comment"]

        self.recipe.change_ingredient_comment(self.ingredient, comment)
        self.ingredient.comment = comment

        if turbo.can_stream():
            return turbo.stream(
                turbo.replace(
                    self.template(template_name="_row"),
                    target=f"ingredient-{self.ingredient.id}",
                )
            )
        else:
            return redirect(url_for("RecipesView:edit", id=self.recipe.id))

    @route("change_measured/<recipe_id>/<ingredient_id>/<measured>", methods=["POST"])
    def change_ingredient_measured(self, recipe_id, ingredient_id, measured):
        self.ingredient = Ingredient.load(ingredient_id)
        measured = measured == "True"

        self.recipe.change_ingredient_measured(self.ingredient, measured)
        self.ingredient.is_measured = measured
        self.ingredient.amount = self.ingredient.load_amount_by_recipe(self.recipe)

        if turbo.can_stream():
            return turbo.stream(
                turbo.replace(
                    self.template(template_name="_row"),
                    target=f"ingredient-{self.ingredient.id}",
                )
            )
        else:
            return redirect(url_for("RecipesView:edit", id=self.recipe.id))

    @route("remove_ingredient/<recipe_id>/<ingredient_id>", methods=["POST"])
    def remove_ingredient(self, recipe_id, ingredient_id):
        ingredient = Ingredient.load(ingredient_id)

        if not self.recipe.remove_ingredient(ingredient):
            flash("Tato surovina už byla smazána.", "error")
            return redirect(url_for("RecipesView:edit", id=self.recipe.id))

        if turbo.can_stream():
            return turbo.stream(
                [turbo.remove(target=f"ingredient-{ingredient_id}")]
                + self.update_usable_ingredients(self.recipe)
            )
        else:
            return redirect(url_for("RecipesView:edit", id=self.recipe.id))

    @route("refresh_usable_ingredients/<recipe_id>", methods=["POST"])
    def refresh_usable_ingredients(self, recipe_id):
        response = self.update_usable_ingredients(self.recipe)

        if turbo.can_stream():
            return turbo.stream(response)
        else:
            return redirect(url_for("RecipesView:edit", id=self.recipe.id))

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
                target="add_ingredient_form",
            )
        ]
