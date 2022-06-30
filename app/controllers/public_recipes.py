from flask import redirect, url_for, request
from flask import render_template as template
from flask_classful import route
from flask_security import login_required, current_user

from app import turbo

from app.helpers.helper_flask_view import HelperFlaskView

from app.models import Recipe, RecipeCategory, Label
from app.forms import PublicRecipeFilterForm


class PublicRecipeView(HelperFlaskView):
    template_folder = "public_recipes"

    def before_request(self, name, *args, **kwargs):
        self.recipes = Recipe.load_all_public()

    @login_required
    def before_index(self):
        self.form = PublicRecipeFilterForm()

    @login_required
    @route("/react/<recipe_id>", methods=["POST"])
    def toggle_reaction(self, recipe_id, refresh=False):
        recipe = Recipe.load(recipe_id)
        recipe.toggle_reaction()

        refresh = bool(request.args.get("refresh"))

        # TODO: This should be made without turbo, but problem with Bootstrap table
        if turbo.can_stream() and not refresh:
            return turbo.stream(
                turbo.replace(
                    template("public_recipes/_recipe_row.html.j2", recipe=recipe),
                    target=f"recipe-{recipe_id}",
                )
            )

        return redirect(request.referrer)

    @login_required
    @route("/", methods=["GET", "POST"])
    def index(self):
        self.recipes = Recipe.load_all_public()

        # Filter recipes
        if ingredient := self.form.ingredient.data:
            self.recipes = [r for r in self.recipes if ingredient in r.ingredients]

        if self.form.with_reaction.data:
            self.recipes = [r for r in self.recipes if r.has_reaction]

        category = self.form.category.data

        if category and category.name != "---":
            self.recipes = [r for r in self.recipes if r.category == category]

        if dietary_labels := self.form.dietary_labels.data:
            self.recipes = [r for r in self.recipes if r.has_labels(dietary_labels)]

        if difficulty_labels := self.form.difficulty_labels.data:
            self.recipes = [
                r for r in self.recipes if r.has_any_of_labels(difficulty_labels)
            ]

        # TODO: This should be made without turbo, but problem with Bootstrap table
        if turbo.can_stream():
            return turbo.stream(
                turbo.replace(
                    self.template(template_name="_recipes_table"),
                    target="recipes-table",
                )
            )
        else:
            return self.template()

    @route("public-index/")
    def public_index(self):
        if current_user.is_authenticated:
            return redirect(url_for("PublicRecipeView:index"))

        return self.template(template_name="public_index")

    @route("cards")
    @login_required
    def card_index(self, *args, **kwargs):
        self.form = PublicRecipeFilterForm(request.args)

        # filter recipe
        if category := RecipeCategory.load(request.args.get("category")):
            self.recipes = [r for r in self.recipes if r.category == category]

        dietary_labels = [
            Label.load(id) for id in request.args.getlist("dietary_labels")
        ]
        if dietary_labels:
            self.recipes = [r for r in self.recipes if r.has_labels(dietary_labels)]

        difficulty_labels = [
            Label.load(id) for id in request.args.getlist("difficulty_labels")
        ]
        if difficulty_labels:
            self.recipes = [
                r for r in self.recipes if r.has_any_of_labels(difficulty_labels)
            ]

        if name := request.args.get("name"):
            self.recipes = [r for r in self.recipes if name in r.name]

        if request.args.get("favorite") == "1":
            self.recipes = [r for r in self.recipes if r.has_reaction]

        # TODO: sort recipes

        return self.template()

    @route("gallery/")
    def gallery(self):
        self.recipes = Recipe.load_all_public_with_image()

        return self.template()
