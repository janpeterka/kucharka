from flask import request, redirect, url_for, flash
from flask_security import login_required, permissions_required

from flask_classful import route

from app.models.recipe_categories import RecipeCategory

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.admin_view_mixin import AdminViewMixin


class RecipeCategorieView(HelperFlaskView, AdminViewMixin):
    decorators = [login_required, permissions_required("manage-application")]
    template_folder = "recipe_categories"
    attribute_name = "recipe-category"
    plural_attribute_name = "recipe-categories"
    instance_name = "category"

    @login_required
    def before_request(self, name, id=None, *args, **kwargs):
        self.category = RecipeCategory.load(id)
        self.recipe_categories = RecipeCategory.load_all()

    def index(self, edit_id=None):
        self.edit_id = request.args.get("edit_id", None)
        return self.template()

    @route("/show_edit/<id>", methods=["POST"])
    def show_edit(self, id):
        return super().show_edit()

    @route("/hide_edit/<id>", methods=["POST"])
    def hide_edit(self, id):
        return super().hide_edit()

    @route("/update/<id>", methods=["POST"])
    def update(self, id):
        self.category.name = request.form["name"]
        self.category.description = request.form["description"]
        self.category.save()

        return super().update()

    @route("/edit/<id>", methods=["POST"])
    def edit(self, id):
        self.category.name = request.form["recipe-category"]
        self.category.save()

        return super().edit()

    def post(self):
        self.category = RecipeCategory(name=request.form["recipe-category"])
        self.category.save()

        return super().post()

    def delete(self, id):
        if self.category.is_used:
            flash("už je někde použité, nelze smazat!")
            return redirect(url_for("RecipeCategorieView:index"), code=303)

        self.category.delete()
        return super().delete()
