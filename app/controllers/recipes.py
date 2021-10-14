from unidecode import unidecode

# from flask import render_template as template
from flask import request, redirect, url_for, flash

from flask_security import login_required, current_user

from flask_classful import route

from app import turbo

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.form import save_form_to_session, create_form

from app.models.recipes import Recipe
from app.models.ingredients import Ingredient

from app.controllers.forms.recipes import RecipesForm, RecipeFilterForm


class RecipesView(HelperFlaskView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, id=None, **kwargs):
        self.recipe = Recipe.load(id)
        self.validate_operation(id, self.recipe)

        if name in ["index", "filter"]:
            self.recipes = sorted(
                current_user.visible_recipes, key=lambda x: unidecode(x.name.lower())
            )

            self.form = RecipeFilterForm()

        if name in ["show", "pdf", "show_pdf"] and "portion_count" in request.args:
            request_portion_count = request.args.get("portion_count", "1")
            if not request_portion_count:
                request_portion_count = 1

            self.recipe.portion_count = int(request_portion_count)

    def before_filter(self):
        self.form = RecipeFilterForm(request.form)

    def before_edit(self, id):
        self.form = create_form(RecipesForm, obj=self.recipe)

        unused_ingredients = [
            i
            for i in current_user.personal_ingredients
            if i not in self.recipe.ingredients
        ]
        self.personal_ingredients = sorted(
            unused_ingredients, key=lambda x: unidecode(x.name.lower())
        )

        unused_public_ingredients = [
            i for i in Ingredient.load_all_public() if i not in self.recipe.ingredients
        ]
        self.public_ingredients = sorted(
            unused_public_ingredients, key=lambda x: unidecode(x.name.lower())
        )

    def before_new(self):
        self.form = create_form(RecipesForm)

    def index(self):
        return self.template()

    def show(self, id):
        return self.template()

    def show_pdf(self, id):
        return self.template(template_name="show", print=True)

    def pdf(self, id):
        from flask_weasyprint import render_pdf, HTML

        return render_pdf(HTML(string=self.template(template_name="show", print=True)))

    def pdf_download(self, id):
        from flask_weasyprint import render_pdf, HTML
        from app.helpers.general import slugify

        filename = slugify(self.recipe.name)

        return render_pdf(
            HTML(string=self.template(template_name="show", print=True)),
            download_filename=f"{filename}.pdf",
        )

    @route("show_with_portion_count/<id>/", methods=["POST"])
    def show_with_portion_count(self, id):
        portion_count = request.form["portion_count"]
        return redirect(url_for("RecipesView:show", id=id, portion_count=portion_count))

    def edit(self, id):
        return self.template()

    def new(self):
        return self.template()

    @route("delete/<id>/", methods=["POST"])
    def delete(self, id):
        if self.recipe.is_used:
            flash("Recept je použit, nelze smazat.", "error")
            return redirect(url_for("RecipesView:show", id=id))

        self.recipe.delete()
        flash("Recept byl smazán.", "success")
        return redirect(url_for("DashboardView:index"))

    def post(self):
        form = RecipesForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("RecipesView:new"))

        recipe = Recipe(author=current_user)
        form.populate_obj(recipe)

        recipe.save()
        return redirect(url_for("RecipesView:edit", id=recipe.id))

    def duplicate(self, id):
        new_recipe = self.recipe.duplicate()
        return redirect(url_for("RecipesView:show", id=new_recipe.id))

    @route("toggle_shared/<id>", methods=["POST"])
    def toggle_shared(self, id):
        toggled = self.recipe.toggle_shared()
        if toggled is True:
            flash("Recept byl zveřejněn.", "success")
        else:
            flash("Recept byl skryt před veřejností.", "success")
        return redirect(url_for("RecipesView:show", id=self.recipe.id))

    @route("delete_drafts", methods=["POST"])
    def delete_drafts(self):
        for draft in current_user.draft_recipes:
            draft.delete()

        return redirect(url_for("DashboardView:index"))

    @route("filter", methods=["POST"])
    def filter(self):
        self.recipes = current_user.visible_recipes

        # Get filters from request
        labels = self.form.labels.data
        ingredient = self.form.ingredient.data
        category = self.form.category.data

        # Filter recipes
        if ingredient:
            self.recipes = [x for x in self.recipes if ingredient in x.ingredients]

        if category and category.name != "---":
            self.recipes = [x for x in self.recipes if x.category == category]

        if labels:
            self.recipes = [x for x in self.recipes if x.has_labels(labels)]

        if turbo.can_stream():
            return turbo.stream(
                turbo.replace(self.template(template_name="_recipes"), target="recipes")
            )
        else:
            return self.template("index")
