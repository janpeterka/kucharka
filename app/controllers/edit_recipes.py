from flask import request, redirect, url_for
from flask import render_template as template

from flask_classful import route
from flask_security import login_required, current_user


from app import turbo

from app.helpers.form import save_form_to_session

# from app.helpers.turbo_flash import turbo_flash as flash
from app.helpers.helper_flask_view import HelperFlaskView

from app.models.recipes import Recipe
from app.models.ingredients import Ingredient
from app.models.files import RecipeImageFile

from app.controllers.forms.recipes import RecipesForm


class EditRecipeView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "recipes/edit"
    excluded_methods = ["add_ingredient_to_recipe", "update_usable_ingredients"]

    @login_required
    def before_request(self, name, recipe_id, **kwargs):
        self.recipe = Recipe.load(recipe_id)
        self.validate_operation(recipe_id, self.recipe)

    @route("info/<recipe_id>", methods=["POST"])
    def post(self, recipe_id):
        form = RecipesForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("RecipesView:edit", id=self.recipe.id))

        form.populate_obj(self.recipe)

        self.recipe.edit()
        self.recipe.reload()

        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.replace(
                        self.template("_info", message="Upraveno", form=form),
                        target="recipe-info",
                    ),
                    turbo.replace(
                        self.template("_ingredient_table"),
                        target="recipe-ingredient-table",
                    ),
                ]
            )
        else:
            return redirect(url_for("RecipesView:edit", id=self.recipe.id))

    @route("description/<recipe_id>/", methods=["POST"])
    def post_description(self, recipe_id):
        self.recipe.description = request.form["description"]
        self.recipe.edit()

        if turbo.can_stream():
            return turbo.stream(
                turbo.replace(
                    self.template("_description", message="Upraveno"),
                    target="recipe-description",
                )
            )
        else:
            return redirect(url_for("RecipesView:edit", id=self.recipe.id))

    @route("refresh_usable_ingredients/<recipe_id>", methods=["POST"])
    def refresh_usable_ingredients(self, recipe_id):
        if turbo.can_stream():
            return turbo.stream(self.update_usable_ingredients(self.recipe))
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

    @route("/upload-photo/<recipe_id>", methods=["POST"])
    def upload_photo(self, recipe_id):
        photo = RecipeImageFile(recipe_id=recipe_id)
        photo.data = request.files.get("file")
        photo.save()

        return redirect(url_for("RecipesView:show", id=recipe_id))

    @route("/delete-all-photos/<recipe_id>", methods=["POST"])
    def delete_all_photos(self, recipe_id):
        for image in self.recipe.images:
            image.delete()

        return redirect(url_for("RecipesView:show", id=recipe_id))

    @route("/set-main-image/<recipe_id>/<image_id>", methods=["POST"])
    def set_main_image(self, recipe_id, image_id):
        new_image = RecipeImageFile.load(image_id)
        for image in self.recipe.images:
            if image.is_main:
                image.is_main = False
                image.edit()

        new_image.is_main = True
        new_image.edit()

        return redirect(url_for("RecipesView:show", id=recipe_id))
