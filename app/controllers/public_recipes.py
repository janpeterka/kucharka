from app.models.recipes import Recipe

from app import turbo

from flask import render_template as template

from flask import redirect, url_for

from flask_classful import route
from flask_security import login_required, current_user

from app.helpers.helper_flask_view import HelperFlaskView

from app.controllers.forms.public_recipes import PublicRecipeFilterForm


class PublicRecipesView(HelperFlaskView):
    template_folder = "public_recipes"

    def before_request(self, name, *args, **kwargs):
        self.recipes = Recipe.load_all_public()

    @login_required
    def before_index(self):
        self.form = PublicRecipeFilterForm()

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
