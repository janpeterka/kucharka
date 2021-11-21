from flask import flash, request, redirect, url_for


from flask_classful import route
from flask_security import login_required, current_user, permissions_required

from app.helpers.form import save_form_to_session, create_form
from app.helpers.helper_flask_view import HelperFlaskView

from app.models.ingredients import Ingredient
from app.models.recipes import Recipe
from app.models.measurements import Measurement

from app.controllers.forms.ingredients import IngredientsForm


class IngredientsView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "ingredients"

    @login_required
    def before_request(self, name, id=None, *args, **kwargs):
        self.ingredient = Ingredient.load(id)
        self.validate_operation(id, self.ingredient)

    def before_new(self):
        self.form = create_form(IngredientsForm)

    def before_edit(self, id):
        self.form = create_form(IngredientsForm, obj=self.ingredient)

        self.recipes = Recipe.load_by_ingredient_and_user(self.ingredient, current_user)
        self.all_recipes = Recipe.load_by_ingredient(self.ingredient)

    def before_show(self, id):
        self.from_new = request.args.get("from_new", False)

        self.recipes = Recipe.load_by_ingredient_and_user(self.ingredient, current_user)
        self.all_recipes = Recipe.load_by_ingredient(self.ingredient)

        self.possible_alternative_measurements = [
            m
            for m in Measurement.load_all()
            if m not in self.ingredient.used_measurements
        ]

    def before_index(self):
        from unidecode import unidecode

        self.ingredients = current_user.personal_ingredients
        self.ingredients.sort(key=lambda x: unidecode(x.name.lower()))

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

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("IngredientsView:new"))

        ingredient = Ingredient(author=current_user)
        form.populate_obj(ingredient)
        ingredient.save()

        return redirect(
            url_for("IngredientsView:show", id=ingredient.id, from_new=True)
        )

    @route("edit/<id>", methods=["POST"])
    def post_edit(self, id):
        form = IngredientsForm(request.form)

        if not self.ingredient.can_edit_measurement:
            del form.measurement

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("IngredientsView:edit", id=self.ingredient.id))

        form.populate_obj(self.ingredient)
        self.ingredient.edit()

        return redirect(url_for("IngredientsView:show", id=self.ingredient.id))

    @route("delete/<id>", methods=["POST"])
    def delete(self, id):
        if self.ingredient.can_be_deleted:
            self.ingredient.delete()
            flash("Surovina byla smazána", "success")
            return redirect(url_for("IngredientsView:index"))
        else:
            flash("Tato surovina je použita, nelze smazat", "error")
            return redirect(url_for("IngredientsView:show", id=self.ingredient.id))

    @permissions_required("manage-application")
    @route("publish/<id>", methods=["POST"])
    def toggle_public(self, id):
        if self.ingredient.is_public:
            self.ingredient.unpublish()
        else:
            self.ingredient.publish()

        return redirect(url_for("IngredientsView:show", id=self.ingredient.id))
