from unidecode import unidecode

from flask import abort, flash, request, redirect, url_for

# from flask import render_template as template


from flask_classful import route
from flask_security import login_required, current_user

from app import turbo

from app.helpers.form import save_form_to_session
from app.helpers.extended_flask_view import ExtendedFlaskView

# from app.handlers.data import DataHandler

from app.models.ingredients import Ingredient
from app.models.ingredient_categories import IngredientCategory
from app.models.recipes import Recipe
from app.models.measurements import Measurement

from app.controllers.forms.ingredients import IngredientsForm


def set_form(form, ingredient=None):
    measurements = Measurement.load_all()
    # measurements.sort(key=lambda x: unidecode(x.name.lower()))
    categories = IngredientCategory.load_all()
    categories.sort(key=lambda x: unidecode(x.name.lower()))

    if ingredient:
        if ingredient.measurement:
            form.measurement.data = ingredient.measurement.id
        if ingredient.category:
            form.category.data = ingredient.category.id

    form.set_all(measurements=measurements, categories=categories)


class IngredientsView(ExtendedFlaskView):
    decorators = [login_required]
    template_folder = "ingredients"

    def before_request(self, name, id=None, *args, **kwargs):
        super().before_request(name, id, *args, **kwargs)

        if id is not None:
            if self.ingredient is None:
                abort(404)
            if not self.ingredient.can_current_user_view:
                abort(403)

    def before_new(self, *args, **kwargs):
        super().before_new(*args, **kwargs)
        set_form(self.form)

    def before_edit(self, id):
        super().before_edit(id)
        set_form(self.form, self.ingredient)

        self.recipes = Recipe.load_by_ingredient_and_user(self.ingredient, current_user)
        self.all_recipes = Recipe.load_by_ingredient(self.ingredient)

    def before_show(self, id):
        self.from_new = request.args.get("from_new", False)

        self.recipes = Recipe.load_by_ingredient_and_user(self.ingredient, current_user)
        self.all_recipes = Recipe.load_by_ingredient(self.ingredient)

    def before_index(self):
        self.ingredients = [
            i for i in current_user.ingredients if i not in Ingredient.load_all_public()
        ]

    def before_public(self):
        self.public_ingredients = Ingredient.load_all_public()

    @route("/ingredients/show_edit/<ingredient_id>", methods=["POST"])
    def show_edit(self, ingredient_id):
        self.ingredient = Ingredient.load(ingredient_id)

        self.measurements = Measurement.load_all()
        # measurements.sort(key=lambda x: unidecode(x.name.lower()))
        self.categories = IngredientCategory.load_all()
        self.categories.sort(key=lambda x: unidecode(x.name.lower()))

        return turbo.stream(
            turbo.replace(
                self.template(template_name="_edit"),
                target=f"ingredient-{ingredient_id}",
            )
        )

    def post(self):
        form = IngredientsForm(request.form)
        set_form(form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("IngredientsView:new"))

        ingredient = Ingredient(author=current_user)
        form.measurement.data = Measurement.load(form.measurement.data)
        form.category.data = IngredientCategory.load(form.category.data)
        form.populate_obj(ingredient)

        if ingredient.save():
            return redirect(
                url_for("IngredientsView:show", id=ingredient.id, from_new=True)
            )
        else:
            flash("Nepodařilo se vytvořit surovinu", "error")
            return redirect(url_for("IngredientsView:new"))

    @route("ingredients/edit/<id>", methods=["POST"])
    def list_edit(self, id):
        self.ingredient.category = IngredientCategory.load(request.form["category_id"])
        self.ingredient.measurement = Measurement.load(request.form["measurement_id"])

        self.ingredient.save()
        return turbo.stream(
            turbo.replace(
                self.template(template_name="_ingredient"),
                target=f"ingredient-{self.ingredient.id}",
            )
        )

    @route("edit/<id>", methods=["POST"])
    def post_edit(self, id):
        form = IngredientsForm(request.form)
        set_form(form)

        if not self.ingredient.can_edit_measurement:
            del form.measurement

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("IngredientsView:edit", id=self.ingredient.id))

        if self.ingredient.can_edit_measurement:
            form.measurement.data = Measurement.load(form.measurement.data)
        form.category.data = IngredientCategory.load(form.category.data)
        form.populate_obj(self.ingredient)
        self.ingredient.edit()

        return redirect(url_for("IngredientsView:show", id=self.ingredient.id))

    @route("delete/<id>", methods=["POST"])
    def delete(self, id):
        if not self.ingredient.is_used:
            self.ingredient.remove()
            flash("Surovina byla smazána", "success")
            return redirect(url_for("DashboardView:show"))
        else:
            flash("Tato surovina je použita, nelze smazat", "error")
            return redirect(url_for("IngredientsView:show", id=self.ingredient.id))

    def public(self):
        return self.template()
