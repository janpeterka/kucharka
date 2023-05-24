from flask import request, redirect, url_for

from flask_classful import route
from flask_security import login_required, permissions_required

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

    def index(self, highlighted_id=None):
        self.highlighted_id = int(request.args.get("highlighted_id", -1))

        return self.template()

    @route("update/<id>", methods=["POST"])
    def update(self, id):
        from app.forms import IngredientForm

        form = IngredientForm(request.form, obj=self.ingredient)

        self.ingredient.category = form.category.data
        self.ingredient.measurement = form.measurement.data

        self.ingredient.edit()

        return redirect(url_for("PublicIngredientView:index", highlighted_id=id))
