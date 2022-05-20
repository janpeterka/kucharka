from flask import request, redirect, url_for

from flask_classful import route
from flask_security import login_required, permissions_required

from app import turbo

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.ingredients import Ingredient
from app.models.ingredient_categories import IngredientCategory
from app.models.measurements import Measurement


class PublicIngredientView(HelperFlaskView):
    decorators = [login_required, permissions_required("manage-application")]
    template_folder = "ingredients/public"

    def before_request(self, name, id=None, *args, **kwargs):
        self.ingredient = Ingredient.load(id)

        self.measurements = Measurement.load_all()
        self.categories = IngredientCategory.load_all()
        self.public_ingredients = Ingredient.load_all_public()

    def index(self, edit_id=None):
        self.edit_id = int(request.args.get("edit_id", -1))
        return self.template()

    @route("/ingredients/show_edit/<id>", methods=["POST"])
    def show_edit(self, id):
        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.after(
                        self.template(template_name="_edit"),
                        target=f"public-ingredient-{self.ingredient.id}",
                    ),
                    turbo.replace(
                        self.template(template_name="_ingredient", editing=True),
                        target=f"public-ingredient-{self.ingredient.id}",
                    ),
                ]
            )
        else:
            return redirect(
                url_for("PublicIngredientView:index", edit_id=self.ingredient.id)
            )

    @route("ingredients/hide_edit/<id>", methods=["POST"])
    def hide_edit(self, id):
        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.remove(
                        target=f"public-ingredient-edit-{self.ingredient.id}",
                    ),
                    turbo.replace(
                        self.template(template_name="_ingredient"),
                        target=f"public-ingredient-{self.ingredient.id}",
                    ),
                ]
            )
        else:
            return redirect(url_for("PublicIngredientView:index"))

    @route("update/<id>", methods=["POST"])
    def update(self, id):
        self.ingredient.category = IngredientCategory.load(request.form["category_id"])
        self.ingredient.measurement = Measurement.load(request.form["measurement_id"])

        self.ingredient.save()

        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.replace(
                        self.template(template_name="_ingredient"),
                        target=f"public-ingredient-{self.ingredient.id}",
                    ),
                    turbo.remove(target=f"public-ingredient-edit-{self.ingredient.id}"),
                ]
            )
        else:
            return redirect(url_for("PublicIngredientView:index"))
