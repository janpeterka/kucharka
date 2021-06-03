from flask import request
from flask_security import login_required, roles_accepted

from app import turbo

from flask_classful import route

from app.models.ingredient_categories import IngredientCategory

from app.helpers.helper_flask_view import HelperFlaskView


class IngredientCategoriesView(HelperFlaskView):
    decorators = [login_required, roles_accepted("admin", "application_manager")]
    template_folder = "ingredient_categories"

    def before_request(self, name, id=None, *args, **kwargs):
        self.category = IngredientCategory.load(id)

    def before_index(self):
        self.ingredient_categories = IngredientCategory.load_all()

    def index(self):
        return self.template()

    @route("/edit/<id>", methods=["POST"])
    def edit(self, id):
        return turbo.stream(
            turbo.replace(
                self.template(template_name="_edit"), target=f"ingredient-category-{id}"
            )
        )

    def put(self, id):
        self.category.name = request.form["ingredient-category"]
        self.category.save()
        return turbo.stream(
            turbo.replace(
                self.template(template_name="_ingredient_category"),
                target=f"ingredient-category-{id}",
            )
        )

    def post(self):
        self.category = IngredientCategory(name=request.form["ingredient-category"])
        self.category.save()

        return turbo.stream(
            [
                turbo.append(
                    self.template(template_name="_ingredient_category"),
                    target="ingredient-categories",
                ),
                turbo.replace(
                    self.template("_add"), target="ingredient-category-create-form"
                ),
            ]
        )

    def delete(self, id):
        from app.helpers.turbo_flash import turbo_flash

        if self.category.is_used:
            return turbo_flash("Už je někde použité, nelze smazat!")

        self.category.delete()
        return turbo.stream(turbo.remove(target=f"ingredient-category-{id}"))
