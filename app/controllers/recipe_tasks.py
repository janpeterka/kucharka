from flask import request, redirect, url_for
from flask_classful import route

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.form import create_form, save_form_to_session

from app.models import Recipe, RecipeTask
from app.forms import RecipeTaskForm


class RecipeTaskView(HelperFlaskView):
    def before_request(self, name, id=None, *args, **kwargs):
        self.task = RecipeTask.load(id)

    def before_new(self, recipe_id):
        self.recipe = Recipe.load(recipe_id)

    def before_post(self, recipe_id):
        self.recipe = Recipe.load(recipe_id)

    def new(self, recipe_id):
        self.form = create_form(RecipeTaskForm)

        return self.template()

    def post(self, recipe_id):
        form = RecipeTaskForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("RecipeTaskView:new", recipe_id=recipe_id))

        task = RecipeTask(recipe=self.recipe)
        form.populate_obj(task)
        task.save()

        return redirect(url_for("RecipeView:show", id=recipe_id))

    def show(self, id):
        return self.template()

    def edit(self, id):
        self.form = create_form(RecipeTaskForm, obj=self.recipe)

        return self.template()

    @route("update/<id>", methods=["POST"])
    def update(self, id):
        form = RecipeTaskForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("RecipeTaskView:new"))

        form.populate_obj(self.task)
        self.task.edit()

        return redirect(url_for("RecipeView:show", id=self.task.recipe.id))

    @route("delete/<id>", methods=["POST"])
    def delete(self, id):
        self.recipe.remove()

        return redirect(request.referrer)
