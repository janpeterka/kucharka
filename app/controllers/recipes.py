from unidecode import unidecode

from flask import request, redirect, url_for, flash
from flask import current_app as application
from flask_classful import route
from flask_security import login_required, current_user
from flask_weasyprint import render_pdf, HTML

from app.modules.files import PhotoForm

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.form import save_form_to_session, create_form

from app.models import Recipe

from app.forms import RecipeForm, IngredientForm


def get_portion_count(recipe, request):
    request_portion_count = request.args.get("portion_count", None)

    if not request_portion_count:
        request_portion_count = recipe.portion_count

    return float(request_portion_count)


class RecipeView(HelperFlaskView):
    def before_request(self, name, id=None, **kwargs):
        self.recipe = Recipe.load(id)

        if current_user.is_authenticated and self.recipe:
            self.validate_show(self.recipe)

    @login_required
    def index(self):
        self.recipes = sorted(
            current_user.visible_recipes,
            key=lambda x: unidecode(x.name.lower()),
        )

        return self.template()

    @login_required
    def new(self):
        self.form = create_form(RecipeForm)

        return self.template()

    @login_required
    def post(self):
        form = RecipeForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("RecipeView:new"))

        recipe = Recipe(author=current_user)
        recipe.fill(form)
        recipe.save()

        return redirect(url_for("RecipeView:edit", id=recipe.id))

    def show(self, id):
        self.recipe.portion_count = get_portion_count(self.recipe, request)
        self.photo_form = PhotoForm()

        if not current_user.is_authenticated:
            self.validate_show(self.recipe)
            return self.template("show", public=True)

        return self.template()

    @login_required
    def edit(self, id, **kwargs):
        self.editing_id = int(request.args.get("editing_id", 0))
        self.show_fast_add = request.args.get("show_fast_add", False)
        self.highlighted_ingredient_id = int(
            request.args.get("highlighted_ingredient_id", 0)
        )
        self.ingredient_form = IngredientForm()

        self.form = create_form(RecipeForm, obj=self.recipe)

        self.personal_ingredients = sorted(
            self.recipe.unused_personal_ingredients,
            key=lambda x: unidecode(x.name.lower()),
        )

        self.public_ingredients = sorted(
            self.recipe.unused_public_ingredients,
            key=lambda x: unidecode(x.name.lower()),
        )

        return self.template()

    @login_required
    @route("delete/<id>/", methods=["POST"])
    def delete(self, id):
        if self.recipe.is_used:
            flash("recept je použit, nelze smazat.", "error")
            return redirect(url_for("RecipeView:show", id=id))

        self.recipe.delete()
        flash("recept byl smazán.", "success")
        prev_path = request.form["previous"]

        with application.test_client() as tc:
            try:
                response = tc.get(prev_path)
                if response.status_code == 200:
                    return redirect(prev_path)
                else:
                    return redirect(url_for("RecipeView:index"))
            except Exception:
                return redirect(url_for("RecipeView:index"))

    def show_pdf(self, id):
        self.recipe.portion_count = get_portion_count(self.recipe, request)

        return self.template(template_name="show", print=True)

    def pdf(self, id):
        self.recipe.portion_count = get_portion_count(self.recipe, request)

        return render_pdf(HTML(string=self.template(template_name="show", print=True)))

    def pdf_download(self, id):
        return render_pdf(
            HTML(string=self.template(template_name="show", print=True)),
            download_filename=f"{self.recipe.slugified_name}.pdf",
        )

    @route("show_with_portion_count/<id>/", methods=["POST"])
    def show_with_portion_count(self, id):
        portion_count = request.form["portion_count"]

        return redirect(url_for("RecipeView:show", id=id, portion_count=portion_count))

    @login_required
    def duplicate(self, id):
        new_recipe = self.recipe.duplicate()
        method = "edit" if self.recipe.is_current_user_author else "show"
        return redirect(url_for(f"RecipeView:{method}", id=new_recipe.id))

    @login_required
    @route("toggle_shared/<id>", methods=["POST"])
    def toggle_shared(self, id):
        toggled = self.recipe.toggle_shared()
        if toggled is True:
            flash("recept byl zveřejněn.", "success")
        else:
            flash("recept byl skryt před veřejností.", "success")
        return redirect(url_for("RecipeView:show", id=self.recipe.id))
