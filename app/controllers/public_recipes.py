from app.models.recipes import Recipe

from flask import request

from flask_classful import route
from flask_security import login_required

# from flask_login import current_user

from app.helpers.extended_flask_view import ExtendedFlaskView
from app.controllers.forms.public_recipes import PublicRecipeFilterForm


class PublicRecipesView(ExtendedFlaskView):
    decorators = [login_required]

    template_folder = "public_recipes"

    def before_index(self, *args, **kwargs):
        self.recipes = Recipe.load_all_public()
        # Get values for filters
        ingredients = [x.ingredients for x in self.recipes]
        flatten_ingredients = [y for x in ingredients for y in x]
        ingredient_names = [x.name for x in flatten_ingredients]
        self.ingredient_names = ["--všechny--"]
        self.ingredient_names.extend(list(set(ingredient_names)))
        self.ingredient_names.sort()

        if request.method == "GET":
            self.form = PublicRecipeFilterForm(ingredient_names=self.ingredient_names)
        else:
            self.form = PublicRecipeFilterForm(
                request.form, ingredient_names=self.ingredient_names
            )

        # Get filters from request
        ingredient_name = None
        with_reaction = None

        if request.method == "POST":
            if not self.form.ingredient_name.data == "--všechny--":
                ingredient_name = self.form.ingredient_name.data
            with_reaction = self.form.with_reaction.data

        # Filter recipes
        if ingredient_name:
            self.recipes = [
                x for x in self.recipes if ingredient_name in x.concat_ingredients
            ]

        if with_reaction:
            self.recipes = [x for x in self.recipes if x.has_reaction]

    @route("/", methods=["GET", "POST"])
    def index(self):
        return self.template()
