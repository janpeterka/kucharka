import datetime

from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin

from app.presenters import DailyPlanPresenter
from app.models.daily_plans_have_recipes import DailyPlanRecipe
from app.models.mixins.daily_plans.daily_plan_recipes import DailyPlanRecipeMixin
from .mixins.day_mixin import DayMixin


class DailyPlan(
    BaseModel,
    BaseMixin,
    DailyPlanRecipeMixin,
    DayMixin,
    DailyPlanPresenter,
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
        order_by=DailyPlanRecipe.position,
    )

    recipes = db.relationship(
        "Recipe",
        secondary="daily_plans_have_recipes",
        viewonly=True,
        order_by=DailyPlanRecipe.position,
    )

    event = db.relationship("Event", back_populates="daily_plans")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().set_defaults()

    @staticmethod
    def load_by_date_and_event(date, event):
        from app.models.daily_plans import DailyPlan

        return DailyPlan.query.filter_by(date=date, event_id=event.id).first()

    @staticmethod
    def load_active_by_date_and_event(date, event):
        plan = DailyPlan.load_by_date_and_event(date, event)
        if plan and plan.is_active:
            return plan
        else:
            return None

    def duplicate(self, event, **kwargs):
        daily_plan = DailyPlan()
        daily_plan.date = kwargs.get("date", self.date)
        daily_plan.event_id = event.id

        daily_plan.save()

        for old_daily_recipe in self.daily_recipes:
            daily_recipe = old_daily_recipe.duplicate()
            daily_recipe.daily_plan_id = daily_plan.id
            daily_recipe.edit()

        return daily_plan

    @property
    def is_filled(self) -> bool:
        return len(self.daily_recipes) > 0

    @property
    def next(self):
        for plan in self.event.active_daily_plans:
            if plan.date == self.date + datetime.timedelta(days=1):
                return plan

        return None

    @property
    def has_next(self) -> bool:
        return self.next is not None

    @property
    def previous(self):
        for plan in self.event.active_daily_plans:
            if plan.date == self.date - datetime.timedelta(days=1):
                return plan

        return None

    @property
    def has_previous(self) -> bool:
        return self.previous is not None

    @property
    def is_shared(self) -> bool:
        return self.event.is_shared

    @property
    def first_recipe(self):
        if self.daily_recipes:
            return self.daily_recipes[0]
        else:
            return None

    @property
    def last_recipe(self):
        if self.daily_recipes:
            return self.daily_recipes[-1]
        else:
            return None

    @property
    def daily_recipes_without_meal_type(self) -> list:
        return [dr for dr in self.daily_recipes if dr.meal_type is None]

    def order_recipes(self):
        elements = sorted(self.daily_recipes, key=lambda x: x.position)

        for i, element in enumerate(elements, start=1):
            element.position = i

        return elements

    # PERMISSIONS

    def can_edit(self, user):
        return self.event.can_edit(user)
