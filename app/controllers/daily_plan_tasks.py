from flask import request, redirect, url_for
from flask_classful import route

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.form import create_form, save_form_to_session

from app.models import DailyPlan, DailyPlanTask
from app.forms import DailyPlanTaskForm


class DailyPlanTaskView(HelperFlaskView):
    def before_request(self, name, id=None, *args, **kwargs):
        self.task = DailyPlanTask.load(id)

        if self.task:
            self.daily_plan = self.task.daily_plan

    def before_new(self, daily_plan_id):
        self.daily_plan = DailyPlan.load(daily_plan_id)

    def before_post(self, daily_plan_id):
        self.daily_plan = DailyPlan.load(daily_plan_id)

    def new(self, daily_plan_id):
        self.form = create_form(DailyPlanTaskForm)

        return self.template()

    def post(self, daily_plan_id):
        form = DailyPlanTaskForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(
                url_for("DailyPlanTaskView:new", daily_plan_id=daily_plan_id)
            )

        task = DailyPlanTask(daily_plan=self.daily_plan)
        form.populate_obj(task)
        task.save()

        return redirect(url_for("DailyPlanView:show", id=daily_plan_id))

    def show(self, id):
        return self.template()

    def edit(self, id):
        self.form = create_form(DailyPlanTaskForm, obj=self.task)

        return self.template()

    @route("update/<id>", methods=["POST"])
    def update(self, id):
        form = DailyPlanTaskForm(request.form)

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("DailyPlanTaskView:new"))

        form.populate_obj(self.task)
        self.task.edit()

        return redirect(url_for("DailyPlanView:show", id=self.task.daily_plan.id))

    @route("delete/<id>", methods=["POST"])
    def delete(self, id):
        self.task.remove()

        return redirect(request.referrer)
