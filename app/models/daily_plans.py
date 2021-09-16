from app import db

from app.helpers.item_mixin import ItemMixin

from app.models.daily_plans_have_recipes import DailyPlanHasRecipe

from app.models.mixins.daily_plans.daily_plan_loaders import DailyPlanLoaderMixin
from app.models.mixins.daily_plans.daily_plan_recipes import DailyPlanRecipeMixin


class DailyPlan(db.Model, ItemMixin, DailyPlanLoaderMixin, DailyPlanRecipeMixin):
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
        "Recipe", secondary="daily_plans_have_recipes", viewonly=True
    )

    event_id = db.Column(db.ForeignKey(("events.id")))
    event = db.relationship("Event", back_populates="daily_plans")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().set_defaults()

    # @staticmethod
    # def create_if_not_exists(date):
    #     DailyPlan.load_by_date_or_create(date)

    # PROPERTIES

    @property
    def is_active(self) -> bool:
        return len(self.daily_recipes) > 0

    @property
    def weekday(self) -> str:
        from app.helpers.formaters import week_day

        return week_day(self.date)

    @property
    def name(self) -> str:
        return self.weekday

    @property
    def next(self):
        daily_plans = self.event.daily_plans
        for plan in daily_plans:
            if plan.id == self.id + 1:
                return plan
        return None

    @property
    def has_next(self) -> bool:
        return self.next is not None

    @property
    def previous(self):
        daily_plans = self.event.daily_plans
        for plan in daily_plans:
            if plan.id == self.id - 1:
                return plan
        return None

    @property
    def has_previous(self) -> bool:
        return self.previous is not None

    @property
    def is_shared(self) -> bool:
        return self.event.is_shared
