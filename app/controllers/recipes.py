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

    @login_required
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
        set_form(self.form, self.recipe)

    def before_new(self):
        self.categories = RecipeCategory.load_all()
        self.public_ingredients = Ingredient.load_all_public()
        self.personal_ingredients = current_user.ingredients

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
        self.recipe.is_draft = False
        self.recipe.edit()

        return redirect(url_for("RecipesView:show", id=self.recipe.id))

    @route("recipes/<id>/edit_description", methods=["POST"])
    def post_edit_description(self, id):
        description = request.form["description"]

        self.recipe.description = description
        self.recipe.edit()

        return redirect(url_for("RecipesView:show", id=self.recipe.id))

    # def show(self, id):
    #     # from .forms.files import PhotoForm

    #     return template(
    #         "recipes/show.html.j2",
    #         recipe=self.recipe,
    #         # is_print=False,
    #         # photo_form=PhotoForm(),
    #     )

    @route("<id>/delete", methods=["POST"])
    def delete(self, id):
        if self.recipe.is_used:
            flash("Recept je použit, nelze smazat.", "error")
            return redirect(url_for("RecipesView:show", id=id))

        self.recipe.remove()
        flash("Recept byl smazán.", "success")
        return redirect(url_for("DashboardView:show"))

    @route("/save", methods=["POST"])
    def save(self):
        if "recipe_id" in request.form and request.form["recipe_id"]:
            recipe = Recipe.load(request.form["recipe_id"])
        else:
            recipe = Recipe()

        recipe.name = request.form["name"]
        recipe.category = RecipeCategory.load(request.form["category_id"])
        recipe.is_draft = False
        recipe.author = current_user

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

        self.recipe.change_ingredient_amount(self.ingredient, amount)
        self.ingredient.amount = amount

        return turbo.stream(
            turbo.replace(
                self.template(template_name="_edit_ingredient"),
                target=f"ingredient-{self.ingredient.id}",
            )
        )
