# from flask import render_template as template
from flask import request, redirect, url_for, flash, abort, g

from flask_login import login_required, current_user

from flask_classful import route

from app.helpers.extended_flask_view import ExtendedFlaskView
from app.models.recipes import Recipe

# from app.models.users import User
from app.models.ingredients import Ingredient

from app.models.recipes_have_ingredients import RecipeHasIngredient

from app.controllers.base_recipes import BaseRecipesView


class RecipesView(BaseRecipesView, ExtendedFlaskView):
    decorators = [login_required]

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

    def public(self):
        return self.template()

    def new(self):
        self.public_ingredients = Ingredient.load_all_public()

        return self.template("recipes/new.html.j2")

    def post(self):
        # TODO: implemented with ajax now, will change
        pass

    @route("<id>/edit", methods=["POST"])
    def post_edit(self, id):
        self.recipe.name = request.form["name"]
        self.recipe.description = request.form["description"]
        self.recipe.edit()
        self.recipe.refresh()
        flash("Recept byl upraven.", "success")
        return redirect(url_for("RecipesView:show", id=self.recipe.id))

    # def show(self, id):
    #     # from .forms.files import PhotoForm

    #     return template(
    #         "recipes/show.html.j2",
    #         recipe=self.recipe,
    #         # is_print=False,
    #         # photo_form=PhotoForm(),
    #     )

    # def print(self, id):
    #     return template("recipes/show.html.j2", recipe=self.recipe, is_print=True,)

    # def edit(self, id):
    # return template("recipes/edit.html.j2", recipe=self.recipe)

    @route("<id>/delete", methods=["POST"])
    def delete(self, id):
        self.recipe.remove()
        flash("Recept byl smazán.", "success")
        return redirect(url_for("DashboardView:show"))

    @route("/saveRecipeAJAX", methods=["POST"])
    def saveRecipeAJAX(self):
        temp_ingredients = request.json["ingredients"]

        recipe_ingredients = []
        for temp_i in temp_ingredients:
            rhi = RecipeHasIngredient()
            rhi.ingredient_id = temp_i["id"]
            rhi.amount = temp_i["amount"]
            recipe_ingredients.append(rhi)

        recipe = Recipe(name=request.json["name"], author=current_user)

        last_id = recipe.create_and_save(recipe_ingredients)
        return url_for("RecipesView:show", id=last_id)

    @route("/toggle_shared/<id>", methods=["POST"])
    def toggle_shared(self, id):
        toggled = self.recipe.toggle_shared()
        print(self.recipe.is_shared)
        if toggled is True:
            flash("Recept byl zveřejněn.", "success")
        else:
            flash("Recept byl skryt před veřejností.", "success")
        return redirect(url_for("RecipesView:show", id=self.recipe.id))
