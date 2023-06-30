from flask import request, redirect, url_for

from flask_classful import route
from flask_security import login_required

from app.helpers.helper_flask_view import HelperFlaskView

from app.models import Recipe, RecipeImageFile


class EditRecipeView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "recipes/edit"

    @login_required
    def before_request(self, name, recipe_id, **kwargs):
        self.recipe = Recipe.load(recipe_id)
        self.validate_edit(self.recipe)

    @route("/upload-photo/<recipe_id>", methods=["POST"])
    def upload_photo(self, recipe_id):
        photo = RecipeImageFile(recipe_id=recipe_id)
        photo.data = request.files.get("file")
        photo.save()

        return redirect(url_for("RecipeView:show", id=recipe_id))

    @route("/delete-all-photos/<recipe_id>", methods=["POST"])
    def delete_all_photos(self, recipe_id):
        for image in self.recipe.images:
            image.delete()

        return redirect(url_for("RecipeView:show", id=recipe_id))

    @route("/set-main-image/<recipe_id>/<image_id>", methods=["POST"])
    def set_main_image(self, recipe_id, image_id):
        new_image = RecipeImageFile.load(image_id)
        for image in self.recipe.images:
            if image.is_main:
                image.is_main = False
                image.edit()

        new_image.is_main = True
        new_image.edit()

        return redirect(url_for("RecipeView:show", id=recipe_id))
