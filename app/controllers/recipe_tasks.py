from flask import request, redirect, url_for
from flask_classful import route

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.form import create_form, save_form_to_session

from app.models import Recipe, RecipeTask
from app.forms import RecipeTaskForm


class RecipeTaskView(HelperFlaskView):
    def before_request(self, name, id=None, *args, **kwargs):
        self.task = RecipeTask.load(id)

        if self.task:
            self.recipe = self.task.recipe

    def before_new(self, recipe_id):
        self.recipe = Recipe.load(recipe_id)
        self.validate_edit(self.recipe)

    def before_post(self, recipe_id):
        self.recipe = Recipe.load(recipe_id)
        self.validate_edit(self.recipe)

    def before_edit(self, id):
        self.validate_edit(self.task)

    def before_update(self, id):
        self.validate_edit(self.task)

    def before_delete(self, id):
        self.validate_delete(self.task)

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
        self.form = create_form(RecipeTaskForm, obj=self.task)

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
        self.task.remove()

        return redirect(request.referrer)
