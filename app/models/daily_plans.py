import datetime

from app import db, BaseModel

from app.helpers.item_mixin import ItemMixin

from app.models.daily_plans_have_recipes import DailyPlanHasRecipe

from app.models.mixins.daily_plans.daily_plan_loaders import DailyPlanLoaderMixin
from app.models.mixins.daily_plans.daily_plan_recipes import DailyPlanRecipeMixin


class DailyPlan(BaseModel, ItemMixin, DailyPlanLoaderMixin, DailyPlanRecipeMixin):
    __tablename__ = "daily_plans"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)

    created_by = db.Column(db.ForeignKey(("users.id")), nullable=False, index=True)
    author = db.relationship("User", uselist=False, back_populates="daily_plans")

    daily_recipes = db.relationship(
        "DailyPlanHasRecipe",
        back_populates="daily_plan",
        cascade="all,delete",
        order_by=DailyPlanHasRecipe.order_index,
    )

    recipes = db.relationship(
        "Recipe",
        secondary="daily_plans_have_recipes",
        viewonly=True,
        order_by=DailyPlanHasRecipe.order_index,
    )

    event_id = db.Column(db.ForeignKey(("events.id")))
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

    # @staticmethod
    # def create_if_not_exists(date):
    #     DailyPlan.load_by_date_or_create(date)

    # PROPERTIES

    @property
    def is_filled(self) -> bool:
        return len(self.daily_recipes) > 0

    @property
    def is_active(self) -> bool:
        return self in self.event.active_daily_plans

    @property
    def weekday(self) -> str:
        from app.helpers.formaters import week_day

        return week_day(self.date)

    @property
    def week(self) -> int:
        return int(self.date.strftime("%V"))

    @property
    def name(self) -> str:
        return self.weekday

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

    def can_edit(self, user):
        return self.event.can_edit(user)
