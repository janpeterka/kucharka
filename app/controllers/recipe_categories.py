from flask import request
from flask_security import login_required

from app import turbo

from flask_classful import route

from app.models.recipe_categories import RecipeCategory

from app.helpers.auth import admin_required
from app.helpers.extended_flask_view import ExtendedFlaskView


class RecipeCategoriesView(ExtendedFlaskView):
    decorators = [login_required, admin_required]

    def before_request(self, name, id=None, *args, **kwargs):
        super().before_request(name, id, *args, **kwargs)
        self.recipe_categories = RecipeCategory.load_all()

        if id:
            self.category = RecipeCategory.load(id)

    @route("/show_edit/<id>", methods=["POST"])
    def show_edit(self, id):
        # Use this while edit:GET doesn't support stream (probably until WebSocket support)
        return turbo.stream(
            turbo.replace(
                self.template(template_name="_edit"), target=f"recipe-category-{id}"
            )
        )

    @route("/edit/<id>", methods=["GET", "POST"])
    def edit(self, id):
        if request.method == "POST":
            self.category.name = request.form["recipe-category"]
            self.category.save()
            return turbo.stream(
                turbo.replace(
                    self.template(template_name="_recipe_category"),
                    target=f"recipe-category-{id}",
                )
            )

        # WIP - move show_edit for "GET" when support for WebSocket

        else:
            return self.template(template_name="index", edit_id=id)

    @route("/create/", methods=["POST"])
    def create(self):
        self.category = RecipeCategory(name=request.form["recipe-category"])
        self.category.save()

        return turbo.stream(
            [
                turbo.append(
                    self.template(template_name="_recipe_category"),
                    target="recipe-categories",
                ),
                turbo.update(
                    self.template(template_name="_add"),
                    target="recipe-category-create-form",
                ),
            ]
        )

    @route("/delete/<id>", methods=["POST"])
    def delete(self, id):
        from app.helpers.turbo_flash import turbo_flash

        if self.category.is_used:
            return turbo_flash("Už je někde použité, nelze smazat!")

        self.category.delete()
        return turbo.stream(turbo.remove(target=f"recipe-category-{id}"))
