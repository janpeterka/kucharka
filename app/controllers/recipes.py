from unidecode import unidecode

# from flask import render_template as template
from flask import request, redirect, url_for, flash

from flask_security import login_required, current_user

from flask_classful import route

from app import turbo

# from app.helpers.extended_flask_view import ExtendedFlaskView
from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.form import save_form_to_session

from app.models.recipes import Recipe
from app.models.ingredients import Ingredient
from app.models.recipe_categories import RecipeCategory

from app.controllers.forms.recipes import RecipesForm, RecipeFilterForm


def set_form(form, recipe=None):
    categories = RecipeCategory.load_all()
    categories.sort(key=lambda x: unidecode(x.name.lower()))

    if recipe:
        if recipe.category:
            form.category.data = recipe.category.id

    form.set_all(categories=categories)


class RecipesView(HelperFlaskView):
    decorators = [login_required]

    def before_request(self, name, id=None, **kwargs):
        # super().before_request(name, id, **kwargs)
        self.recipe = Recipe.load(id)
        self.validate_operation(id, self.recipe)

        if name in ["index", "filter"]:
            self.recipes = current_user.recipes
            ingredients = [x.ingredients for x in self.recipes]
            flatten_ingredients = [y for x in ingredients for y in x]
            ingredient_names = [x.name for x in flatten_ingredients]
            self.ingredient_names = ["---"]
            self.ingredient_names.extend(list(set(ingredient_names)))
            self.ingredient_names.sort()

            self.categories = RecipeCategory.load_all()

            self.form = RecipeFilterForm(
                ingredient_names=self.ingredient_names, categories=self.categories
            )

    def before_filter(self):
        self.form = RecipeFilterForm(
            request.form,
            ingredient_names=self.ingredient_names,
            categories=self.categories,
        )

    def before_edit(self, id):
        self.form = RecipesForm(obj=self.recipe)
        self.categories = RecipeCategory.load_all()

        unused_ingredients = [
            i for i in current_user.ingredients if i not in self.recipe.ingredients
        ]

        unused_public_ingredients = [
            i for i in Ingredient.load_all_public() if i not in self.recipe.ingredients
        ]

        self.public_ingredients = unused_public_ingredients
        self.public_ingredients.sort(key=lambda x: unidecode(x.name.lower()))
        self.personal_ingredients = unused_ingredients
        self.personal_ingredients.sort(key=lambda x: unidecode(x.name.lower()))

        set_form(self.form, self.recipe)

    def before_new(self):
        self.form = RecipesForm()
        self.categories = RecipeCategory.load_all()
        self.public_ingredients = Ingredient.load_all_public()
        self.personal_ingredients = current_user.ingredients
        set_form(self.form)

    def index(self):
        return self.template()

    def show(self, id):
        return self.template()

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
        set_form(form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("RecipesView:new"))

        recipe = Recipe(author=current_user)
        form.category.data = RecipeCategory.load(form.category.data)
        form.populate_obj(recipe)

        recipe.save()
        return redirect(url_for("RecipesView:show", id=recipe.id))

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
        self.recipes = current_user.recipes

        # Get filters from request
        ingredient_name = None
        category = None

        is_vegetarian = self.form.is_vegetarian.data
        is_vegan = self.form.is_vegan.data
        lactose_free = self.form.lactose_free.data
        gluten_free = self.form.gluten_free.data

        if not self.form.ingredient_name.data == "---":
            ingredient_name = self.form.ingredient_name.data

        category = RecipeCategory.load(self.form.category.data)

        # Filter recipes
        if ingredient_name:
            self.recipes = [
                x for x in self.recipes if ingredient_name in x.concat_ingredients
            ]

        if category.name != "---":
            self.recipes = [x for x in self.recipes if x.category == category]

        if is_vegetarian:
            self.recipes = [x for x in self.recipes if x.is_vegetarian]

        if is_vegan:
            self.recipes = [x for x in self.recipes if x.is_vegan]

        if lactose_free:
            self.recipes = [x for x in self.recipes if x.lactose_free]

        if gluten_free:
            self.recipes = [x for x in self.recipes if x.gluten_free]

        return turbo.stream(
            turbo.replace(self.template(template_name="_recipes"), target="recipes")
        )
