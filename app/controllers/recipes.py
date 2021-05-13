from unidecode import unidecode

# from flask import render_template as template
from flask import request, redirect, url_for, flash, abort, g

from flask_security import login_required, current_user

from flask_classful import route

from app import turbo

from app.helpers.extended_flask_view import ExtendedFlaskView
from app.helpers.form import save_form_to_session

from app.models.recipes import Recipe
from app.models.ingredients import Ingredient
from app.models.recipe_categories import RecipeCategory

from app.controllers.base_recipes import BaseRecipesView

from app.controllers.forms.recipes import RecipesForm


def set_form(form, recipe=None):
    categories = RecipeCategory.load_all()
    categories.sort(key=lambda x: unidecode(x.name.lower()))

    if recipe:
        if recipe.category:
            form.category.data = recipe.category.id

    form.set_all(categories=categories)


class RecipesView(BaseRecipesView, ExtendedFlaskView):
    decorators = [login_required]
    template_folder = "recipes"

    def before_request(self, name, id=None, **kwargs):
        g.request_item_type = "recipe"
        if id is not None:
            g.request_item_id = id
            self.recipe = Recipe.load(id)

            if self.recipe is None:
                abort(404)
            if not self.recipe.can_current_user_show:
                abort(403)

    def before_public(self):
        self.public_recipes = Recipe.load_all_public()

    def before_edit(self, id):
        super().before_edit(id)
        self.categories = RecipeCategory.load_all()

        unused_ingredients = [
            i for i in current_user.ingredients if i not in self.recipe.ingredients
        ]

        unused_public_ingredients = [
            i for i in Ingredient.load_all_public() if i not in self.recipe.ingredients
        ]

        self.public_ingredients = unused_public_ingredients
        self.public_ingredients.sort(key=lambda x: unidecode(x.name.lower()))
        self.personal_ingredients = unused_ingredients
        self.personal_ingredients.sort(key=lambda x: unidecode(x.name.lower()))

        set_form(self.form, self.recipe)

    def before_new(self):
        super().before_new()
        self.categories = RecipeCategory.load_all()
        self.public_ingredients = Ingredient.load_all_public()
        self.personal_ingredients = current_user.ingredients
        set_form(self.form)

    def public(self):
        return self.template()

    @route("recipes/edit/<id>", methods=["POST"])
    def post_edit(self, id):
        form = RecipesForm(request.form)
        set_form(form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("RecipesView:edit", id=self.recipe.id))

        form.category.data = RecipeCategory.load(form.category.data)
        form.populate_obj(self.recipe)
        self.recipe.edit()

        return redirect(url_for("RecipesView:show", id=self.recipe.id))

    @route("recipes/<id>/edit_description", methods=["POST"])
    def post_edit_description(self, id):
        description = request.form["description"]

        self.recipe.description = description
        self.recipe.edit()

        return redirect(url_for("RecipesView:show", id=self.recipe.id))

    @route("<id>/delete", methods=["POST"])
    def delete(self, id):
        if self.recipe.is_used:
            flash("Recept je použit, nelze smazat.", "error")
            return redirect(url_for("RecipesView:show", id=id))

        self.recipe.remove()
        flash("Recept byl smazán.", "success")
        return redirect(url_for("DashboardView:show"))

    def post(self):
        form = RecipesForm(request.form)
        set_form(form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("RecipesView:new"))

        recipe = Recipe(author=current_user)
        form.category.data = RecipeCategory.load(form.category.data)
        form.populate_obj(recipe)

        recipe.save()
        return redirect(url_for("RecipesView:show", id=recipe.id))

    @route("/toggle_shared/<id>", methods=["POST"])
    def toggle_shared(self, id):
        toggled = self.recipe.toggle_shared()
        if toggled is True:
            flash("Recept byl zveřejněn.", "success")
        else:
            flash("Recept byl skryt před veřejností.", "success")
        return redirect(url_for("RecipesView:show", id=self.recipe.id))

    @route("/delete_drafts", methods=["POST"])
    def delete_drafts(self):
        for draft in current_user.draft_recipes:
            draft.delete()

        return redirect(url_for("DashboardView:show"))

    @route("/remove_ingredient/<recipe_id>/<ingredient_id>", methods=["POST"])
    def remove_ingredient(self, recipe_id, ingredient_id):
        recipe = Recipe.load(recipe_id)
        ingredient = Ingredient.load(ingredient_id)

        recipe.remove_ingredient(ingredient)
        return turbo.stream(
            [turbo.remove(target=f"ingredient-{ingredient_id}")]
            + BaseRecipesView().update_usable_ingredients(recipe)
        )

    @route("/change_ingredient_amount/<recipe_id>/<ingredient_id>", methods=["POST"])
    def change_ingredient_amount(self, recipe_id, ingredient_id):
        self.recipe = Recipe.load(recipe_id)
        self.ingredient = Ingredient.load(ingredient_id)
        amount = request.form["amount"]

        amount_for_portion = int(amount) / float(self.recipe.portion_count)

        self.recipe.change_ingredient_amount(self.ingredient, amount_for_portion)
        self.ingredient.amount = amount_for_portion

        return turbo.stream(
            turbo.replace(
                self.template(template_name="_edit_ingredient"),
                target=f"ingredient-{self.ingredient.id}",
            )
        )
