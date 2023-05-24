from flask import request, redirect, url_for, flash

from flask_classful import route
from flask_security import login_required, permissions_required, current_user

from app.helpers.helper_flask_view import HelperFlaskView

from app.models import Ingredient
from app.forms import IngredientForm


class PublicIngredientView(HelperFlaskView):
    decorators = [login_required, permissions_required("manage-application")]
    template_folder = "ingredients/public"

    def before_request(self, name, id=None, *args, **kwargs):
        if id:
            self.ingredient = Ingredient.load(id)

    def index(self, highlighted_id=None):
        self.public_ingredients = Ingredient.load_all_public()
        self.highlighted_id = int(request.args.get("highlighted_id", -1))

        return self.template()

    def new(self):
        self.form = IngredientForm()

        return self.template()

    @route("post", methods=["POST"])
    def post(self):
        form = IngredientForm(request.form)

        if not form.validate_on_submit():
            return self.template("new"), 422

        ingredient = Ingredient()
        form.populate_obj(ingredient)
        ingredient.is_public = True
        ingredient.author = current_user
        ingredient.save()

        flash("surovina přidána", "success")

        return redirect(url_for("PublicIngredientView:index"))

    @route("update/<id>", methods=["POST"])
    def update(self, id):
        from app.forms import IngredientForm

        form = IngredientForm(request.form, obj=self.ingredient)

        self.ingredient.category = form.category.data
        self.ingredient.measurement = form.measurement.data

        self.ingredient.edit()

        return redirect(url_for("PublicIngredientView:index", highlighted_id=id))
