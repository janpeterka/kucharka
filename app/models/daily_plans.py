import datetime

from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin

from app.presenters import DailyPlanPresenter

from app.models.daily_plans_have_recipes import DailyPlanRecipe

from app.models.mixins.daily_plans.daily_plan_loaders import DailyPlanLoaderMixin
from app.models.mixins.daily_plans.daily_plan_recipes import DailyPlanRecipeMixin


class DailyPlan(
    BaseModel, BaseMixin, DailyPlanLoaderMixin, DailyPlanRecipeMixin, DailyPlanPresenter
):
    __tablename__ = "daily_plans"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)

    created_by = db.Column(db.ForeignKey(("users.id")), nullable=False, index=True)
    author = db.relationship("User", uselist=False, back_populates="daily_plans")

    event_id = db.Column(db.ForeignKey(("events.id")))

    daily_recipes = db.relationship(
        "DailyPlanRecipe",
        back_populates="daily_plan",
        cascade="all, delete",
        order_by=DailyPlanRecipe.order_index,
    )

    recipes = db.relationship(
        "Recipe",
        secondary="daily_plans_have_recipes",
        viewonly=True,
        order_by=DailyPlanRecipe.order_index,
    )

    event = db.relationship("Event", back_populates="daily_plans")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().set_defaults()

    def duplicate(self):
        daily_plan = DailyPlan()
        daily_plan.date = self.date

        daily_plan.save()

        for old_daily_recipe in self.daily_recipes:
            daily_recipe = old_daily_recipe.duplicate()
            daily_recipe.daily_plan_id = daily_plan.id
            daily_recipe.edit()

        return daily_plan

    # DATA
    @property
    def all_tasks(self) -> list:
        tasks = []

        for daily_plan in self.event.daily_plans:
            if daily_plan.date >= self.date:
                for daily_recipe in daily_plan.daily_recipes:
                    tasks.extend(
                        task
                        for task in daily_recipe.tasks
                        if (
                            self.date
                            == daily_recipe.daily_plan.date
                            - datetime.timedelta(task.days_before_cooking)
                        )
                    )

        tasks.extend(self.tasks)
        return tasks

    # PROPERTIES

    @property
    def is_filled(self) -> bool:
        return len(self.daily_recipes) > 0

    @property
    def is_active(self) -> bool:
        return self in self.event.active_daily_plans

    @property
    def next(self):
        return next(
            (
                plan
                for plan in self.event.active_daily_plans
                if plan.date == self.date + datetime.timedelta(days=1)
            ),
            None,
        )

    @property
    def has_next(self) -> bool:
        return self.next is not None

    @property
    def previous(self):
        return next(
            (
                plan
                for plan in self.event.active_daily_plans
                if plan.date == self.date - datetime.timedelta(days=1)
            ),
            None,
        )

    @property
    def has_previous(self) -> bool:
        return self.previous is not None

    @property
    def is_shared(self) -> bool:
        return self.event.is_shared

    @property
    def first_recipe(self):
        return self.daily_recipes[0] if self.daily_recipes else None

    @property
    def last_recipe(self):
        return self.daily_recipes[-1] if self.daily_recipes else None

    @property
    def daily_recipes_without_meal_type(self) -> list:
        return [dr for dr in self.daily_recipes if dr.meal_type is None]

    # PERMISSIONS

    def can_edit(self, user):
        return self.event.can_edit(user)
