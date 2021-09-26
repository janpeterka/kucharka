from app.models.recipes import Recipe

from app import turbo

from flask import render_template as template

from flask import redirect, url_for

from flask_classful import route
from flask_security import login_required, current_user

from app.helpers.helper_flask_view import HelperFlaskView

from app.controllers.forms.public_recipes import PublicRecipeFilterForm


class PublicRecipesView(HelperFlaskView):
    # decorators = [login_required]
    template_folder = "public_recipes"

    def before_request(self, name, *args, **kwargs):
        self.recipes = Recipe.load_all_public()

    @login_required
    def before_index(self):
        # Get values for filters
        # TODO: tohle mi nepřijde úplně šťastný
        # TODO: načítání by mohlo být přes /src
        ingredients = [x.ingredients for x in self.recipes]
        flatten_ingredients = [y for x in ingredients for y in x]
        ingredient_names = [x.name for x in flatten_ingredients]

        self.ingredient_names = ["---", *list(set(ingredient_names))]
        self.ingredient_names.sort()

        self.form = PublicRecipeFilterForm(ingredient_names=self.ingredient_names)

    @login_required
    @route("/toggleReaction/<recipe_id>", methods=["POST"])
    def toggle_reaction(self, recipe_id):
        from flask import flash

        recipe = Recipe.load(recipe_id)
        recipe.toggle_reaction()

        if turbo.can_stream():
            return turbo.stream(
                turbo.replace(
                    template("public_recipes/_recipe_row.html.j2", recipe=recipe),
                    target=f"recipe-{recipe_id}",
                )
            )
        flash("Reakce byla zaznamenána.")
        return "", 204

    @login_required
    @route("/", methods=["GET", "POST"])
    def index(self):
        self.recipes = Recipe.load_all_public()

        # Get filters from request
        ingredient_name = None

        is_vegetarian = self.form.is_vegetarian.data
        is_vegan = self.form.is_vegan.data
        lactose_free = self.form.lactose_free.data
        gluten_free = self.form.gluten_free.data

        if self.form.ingredient_name.data != "---":
            ingredient_name = self.form.ingredient_name.data

        with_reaction = self.form.with_reaction.data
        category = self.form.category.data

        # Filter recipes
        if ingredient_name:
            self.recipes = [
                x for x in self.recipes if ingredient_name in x.concat_ingredients
            ]

        if with_reaction:
            self.recipes = [x for x in self.recipes if x.has_reaction]

        if category and category.name != "---":
            self.recipes = [x for x in self.recipes if x.category == category]

        if is_vegetarian:
            self.recipes = [x for x in self.recipes if x.is_vegetarian]

        if is_vegan:
            self.recipes = [x for x in self.recipes if x.is_vegan]

        if lactose_free:
            self.recipes = [x for x in self.recipes if x.lactose_free]

        if gluten_free:
            self.recipes = [x for x in self.recipes if x.gluten_free]

        if turbo.can_stream():
            return turbo.stream(
                turbo.replace(
                    self.template(template_name="_recipes_table_body"), target="recipes"
                )
            )
        else:
            return self.template()

    def public_index(self):
        if current_user.is_authenticated:
            return redirect(url_for("PublicRecipesView:index"))

        return self.template(template_name="public_index")
