from app.models.recipes import Recipe

from app import turbo

from flask import request
from flask import render_template as template

from flask_classful import route
from flask_security import login_required

from app.helpers.extended_flask_view import ExtendedFlaskView

from app.models.recipe_categories import RecipeCategory
from app.controllers.forms.public_recipes import PublicRecipeFilterForm


class PublicRecipesView(ExtendedFlaskView):
    decorators = [login_required]

    template_folder = "public_recipes"

    def before_request(self, name, *args, **kwargs):
        self.recipes = Recipe.load_all_public()
        # Get values for filters
        # TODO - tohle mi nepřijde úplně šťastný
        if name in ["index", "filter"]:
            ingredients = [x.ingredients for x in self.recipes]
            flatten_ingredients = [y for x in ingredients for y in x]
            ingredient_names = [x.name for x in flatten_ingredients]
            self.ingredient_names = ["---"]
            self.ingredient_names.extend(list(set(ingredient_names)))
            self.ingredient_names.sort()

            self.categories = RecipeCategory.load_all()

            self.form = PublicRecipeFilterForm(
                ingredient_names=self.ingredient_names, categories=self.categories
            )

    def before_filter(self):
        self.form = PublicRecipeFilterForm(
            request.form,
            ingredient_names=self.ingredient_names,
            categories=self.categories,
        )

    # @route("/", methods=["GET", "POST"])
    # def index(self):
    # return self.template()

    @route("/toggleReaction/<recipe_id>", methods=["POST"])
    def toggle_reaction(self, recipe_id):
        recipe = Recipe.load(recipe_id)
        recipe.toggle_reaction()
        return turbo.stream(
            turbo.replace(
                template("public_recipes/_recipe_row.html.j2", recipe=recipe),
                target=f"recipe-{recipe_id}",
            )
        )

    @route("filter", methods=["POST"])
    def filter(self):
        self.recipes = Recipe.load_all_public()

        # Get filters from request
        ingredient_name = None
        category = None
        with_reaction = None

        is_vegetarian = self.form.is_vegetarian.data
        is_vegan = self.form.is_vegan.data
        without_lactose = self.form.without_lactose.data
        without_gluten = self.form.without_gluten.data

        if not self.form.ingredient_name.data == "---":
            ingredient_name = self.form.ingredient_name.data

        with_reaction = self.form.with_reaction.data

        category = RecipeCategory.load(self.form.category.data)

        # Filter recipes
        if ingredient_name:
            self.recipes = [
                x for x in self.recipes if ingredient_name in x.concat_ingredients
            ]

        if with_reaction:
            self.recipes = [x for x in self.recipes if x.has_reaction]

        if category.name != "---":
            self.recipes = [x for x in self.recipes if x.category == category]

        if is_vegetarian:
            self.recipes = [x for x in self.recipes if x.is_vegetarian]

        if is_vegan:
            self.recipes = [x for x in self.recipes if x.is_vegan]

        if without_lactose:
            self.recipes = [x for x in self.recipes if x.without_lactose]

        if without_gluten:
            self.recipes = [x for x in self.recipes if x.without_gluten]

        return turbo.stream(
            turbo.replace(
                self.template(
                    template_name="public_recipes/_recipes_table_body.html.j2"
                ),
                target="recipes",
            )
        )
