from flask import request, redirect, url_for
from flask_security import login_required, roles_accepted

from app import turbo

from flask_classful import route

from app.models.recipe_categories import RecipeCategory

from app.helpers.helper_flask_view import HelperFlaskView


class RecipeCategoriesView(HelperFlaskView):
    decorators = [login_required, roles_accepted("admin", "application_manager")]
    template_folder = "recipe_categories"

    @login_required
    def before_request(self, name, id=None, *args, **kwargs):
        self.category = RecipeCategory.load(id)
        self.recipe_categories = RecipeCategory.load_all()

    def index(self, edit_id=None):
        self.edit_id = request.args.get("edit_id", None)
        return self.template()

    @route("/show_edit/<id>", methods=["POST"])
    def show_edit(self, id):
        if turbo.can_stream():
            return turbo.stream(
                turbo.replace(
                    self.template(template_name="_edit"), target=f"recipe-category-{id}"
                )
            )
        else:
            return redirect(url_for("RecipeCategoriesView:index", edit_id=id))

    @route("/edit/<id>", methods=["POST"])
    def edit(self, id):
        self.category.name = request.form["recipe-category"]
        self.category.save()

        if turbo.can_stream():
            return turbo.stream(
                turbo.replace(
                    self.template(template_name="_recipe_category"),
                    target=f"recipe-category-{id}",
                )
            )

        else:
            return redirect(url_for("RecipeCategoriesView:index"))

    def post(self):
        self.category = RecipeCategory(name=request.form["recipe-category"])
        self.category.save()

        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.append(
                        self.template(template_name="_recipe_category"),
                        target="recipe-categories",
                    ),
                    turbo.replace(
                        self.template(template_name="_add"),
                        target="recipe-category-create-form",
                    ),
                ]
            )
        else:
            return redirect(url_for("RecipeCategoriesView:index"))

    @route("/delete/<id>", methods=["POST"])
    def delete(self, id):
        from flask import flash
        from app.helpers.turbo_flash import turbo_flash

        if self.category.is_used:
            if turbo.can_stream():
                return turbo_flash("Už je někde použité, nelze smazat!")
            else:
                flash("Už je někde použité, nelze smazat!")
                return redirect(url_for("RecipeCategoriesView:index"))

        else:
            self.category.delete()

            if turbo.can_stream():
                return turbo.stream(turbo.remove(target=f"recipe-category-{id}"))
            else:
                return redirect(url_for("RecipeCategoriesView:index"))
