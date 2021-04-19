from flask import render_template as template
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

    # def index(self):
    # return self.template()

    def new(self):
        # ingredients = Ingredient.load_all_by_author(current_user)
        # shared_ingredients = Ingredient.load_all_shared(renamed=True)

        # TODO - this causes duplication for admin. shouldn't be problem for users.
        # all_ingredients = ingredients + shared_ingredients
        return template(
            "recipes/new.html.j2",
            # ingredients=current_,
            # preset_ingredients=request.args.get("preset_ingredient_ids", []),
        )

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
