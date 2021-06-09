from unidecode import unidecode

from flask import flash, request, redirect, url_for


from flask_classful import route
from flask_security import login_required, current_user, roles_accepted, roles_required

from app.helpers.form import save_form_to_session
from app.helpers.helper_flask_view import HelperFlaskView

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

    form.set_all(measurements=measurements, categories=categories)

    if ingredient:
        if ingredient.measurement:
            form.measurement.data = ingredient.measurement.id
        if ingredient.category:
            form.category.data = ingredient.category.id


class IngredientsView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "ingredients"

    def before_request(self, name, id=None, *args, **kwargs):
        self.ingredient = Ingredient.load(id)
        self.validate_operation(id, self.ingredient)

    def before_new(self):
        self.form = IngredientsForm()
        set_form(self.form)

    def before_edit(self, id):
        self.form = IngredientsForm(obj=self.ingredient)
        set_form(self.form, self.ingredient)

        self.recipes = Recipe.load_by_ingredient_and_user(self.ingredient, current_user)
        self.all_recipes = Recipe.load_by_ingredient(self.ingredient)

    def before_show(self, id):
        self.from_new = request.args.get("from_new", False)

        self.recipes = Recipe.load_by_ingredient_and_user(self.ingredient, current_user)
        self.all_recipes = Recipe.load_by_ingredient(self.ingredient)

    def before_index(self):
        self.ingredients = [
            i
            for i in current_user.personal_ingredients
            if i not in Ingredient.load_all_public()
        ]

    def new(self):
        return self.template()

    def show(self, id):
        return self.template()

    def index(self):
        return self.template()

    def edit(self, id):
        return self.template()

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
            self.ingredient.delete()
            flash("Surovina byla smazána", "success")
            return redirect(url_for("DashboardView:index"))
        else:
            flash("Tato surovina je použita, nelze smazat", "error")
            return redirect(url_for("IngredientsView:show", id=self.ingredient.id))

    @roles_accepted("admin", "application_manager")
    @route("publish/<id>", methods=["POST"])
    def publish(self, id):
        self.ingredient.publish()
        return redirect(url_for("IngredientsView:show", id=self.ingredient.id))

    @roles_required("admin")
    @route("unpublish/<id>", methods=["POST"])
    def unpublish(self, id):
        self.ingredient.unpublish()
        return redirect(url_for("IngredientsView:show", id=self.ingredient.id))
