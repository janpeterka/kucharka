from flask import abort, flash, request, redirect, url_for

# from flask import render_template as template

from flask_classful import route
from flask_login import login_required, current_user

from app.helpers.form import save_form_to_session
from app.helpers.extended_flask_view import ExtendedFlaskView
from app.helpers.auth import admin_required

# from app.handlers.data import DataHandler

from app.models.ingredients import Ingredient
from app.models.recipes import Recipe
from app.models.measurements import Measurement
from app.controllers.forms.ingredients import IngredientsForm


class IngredientsView(ExtendedFlaskView):
    decorators = [login_required]

    def before_request(self, name, id=None, *args, **kwargs):
        super().before_request(name, id, *args, **kwargs)

        if id is not None:
            if self.ingredient is None:
                abort(404)
            if not self.ingredient.can_current_user_view:
                abort(403)

    def before_new(self, *args, **kwargs):
        super().before_new(*args, **kwargs)
        self.form.set_measurement(Measurement.load_all())

    def before_edit(self, id):
        super().before_edit(id)
        self.form.set_measurement(Measurement.load_all())
        self.recipes = Recipe.load_by_ingredient_and_user(self.ingredient, current_user)
        self.all_recipes = Recipe.load_by_ingredient(self.ingredient)

    def before_show(self, id):
        self.recipes = Recipe.load_by_ingredient_and_user(self.ingredient, current_user)
        self.all_recipes = Recipe.load_by_ingredient(self.ingredient)

    def before_index(self):
        self.ingredients = current_user.ingredients

    def before_public(self):
        self.public_ingredients = Ingredient.load_all_public()

    def post(self):
        form = IngredientsForm(request.form)
        form.set_measurement(Measurement.load_all())

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("IngredientsView:new"))

        ingredient = Ingredient(author=current_user)
        form.measurement.data = Measurement.load(form.measurement.data)
        form.populate_obj(ingredient)

        if ingredient.save():
            return redirect(url_for("IngredientsView:show", id=ingredient.id))
        else:
            flash("Nepodařilo se vytvořit surovinu", "error")
            return redirect(url_for("IngredientsView:new"))

    @route("edit/<id>", methods=["POST"])
    def post_edit(self, id):
        form = IngredientsForm(request.form)
        form.set_measurement(Measurement.load_all())

        if self.ingredient.is_used:
            del form.measurement

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("IngredientsView:edit", id=self.ingredient.id))

        form.measurement.data = Measurement.load(form.measurement.data)
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

    @admin_required
    def public(self):
        return self.template(template_name="admin/ingredients/public.html.j2")
