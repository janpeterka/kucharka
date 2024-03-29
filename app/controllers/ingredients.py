from unidecode import unidecode

from flask import flash, request, redirect, url_for
from flask_classful import route
from flask_security import login_required, current_user, permissions_required

from app.helpers.form import save_form_to_session, create_form
from app.helpers.helper_flask_view import HelperFlaskView

from app.models import Ingredient, Recipe, Measurement

from app.forms import IngredientForm


class IngredientView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "ingredients"

    @login_required
    def before_request(self, name, id=None, *args, **kwargs):
        self.ingredient = Ingredient.load(id)

    def before_show(self, id):
        self.validate_show(self.ingredient)

    def before_edit(self, id):
        self.validate_edit(self.ingredient)

    def index(self):
        self.ingredients = current_user.personal_ingredients
        self.ingredients.sort(key=lambda x: unidecode(x.name.lower()))

        return self.template()

    def new(self):
        self.form = create_form(IngredientForm)

        return self.template()

    def show(self, id):
        self.recipes = Recipe.load_by_ingredient_and_user(self.ingredient, current_user)
        self.all_recipes = Recipe.load_by_ingredient(self.ingredient)

        self.possible_alternative_measurements = [
            m
            for m in Measurement.load_all()
            if m not in self.ingredient.used_measurements
        ]

        return self.template()

    def edit(self, id):
        self.form = create_form(IngredientForm, obj=self.ingredient)

        self.recipes = Recipe.load_by_ingredient_and_user(self.ingredient, current_user)
        self.all_recipes = Recipe.load_by_ingredient(self.ingredient)

        return self.template()

    def post(self):
        form = IngredientForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("IngredientView:new"))

        ingredient = Ingredient()
        form.populate_obj(ingredient)
        ingredient.save()

        return redirect(url_for("IngredientView:show", id=ingredient.id))

    @route("update/<id>", methods=["POST"])
    def update(self, id):
        form = IngredientForm(request.form)

        if not self.ingredient.can_edit_measurement:
            del form.measurement

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("IngredientView:edit", id=self.ingredient.id))

        form.populate_obj(self.ingredient)
        self.ingredient.edit()

        return redirect(url_for("IngredientView:show", id=self.ingredient.id))

    @route("delete/<id>", methods=["POST"])
    def delete(self, id):
        if self.ingredient.can_be_deleted:
            self.ingredient.delete()
            flash("surovina byla smazána", "success")
            return redirect(url_for("IngredientView:index"))
        else:
            flash("tato surovina je použita, nelze smazat", "error")
            return redirect(url_for("IngredientView:show", id=self.ingredient.id))

    @permissions_required("manage-application")
    @route("toggle_public/<id>", methods=["POST"])
    def toggle_public(self, id):
        self.ingredient.toggle_public()

        return redirect(url_for("IngredientView:show", id=self.ingredient.id))
