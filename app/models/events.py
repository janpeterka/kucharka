import datetime
from datetime import timedelta
from flask_security import current_user

from app import db, BaseModel
from app.helpers.base_mixin import BaseMixin
from app.helpers.general import list_without_duplicated
from app.presenters import EventPresenter
from app.models import DailyPlan


class Event(BaseModel, BaseMixin, EventPresenter):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80))
    date_from = db.Column(db.Date)
    date_to = db.Column(db.Date)

    people_count = db.Column(db.Integer)

    is_archived = db.Column(db.Boolean, default=False)

    # event is personal, but shared publicly. can change or disappear
    is_shared = db.Column(db.Boolean, default=False)

    created_by = db.Column(db.ForeignKey(("users.id")), nullable=False, index=True)
    author = db.relationship("User", uselist=False, back_populates="events")

    # collaborators = db.relationship(
    #     "User",
    #     secondary="users_have_event_roles",
    #     primaryjoin="and_(Event.id == UserHasEventRole.event_id, UserHasEventRole.role =='collaborator')",
    #     viewonly=True,
    # )

    shared_with = db.relationship(
        "User",
        secondary="users_have_event_roles",
        primaryjoin="Event.id == UserHasEventRole.event_id",
        viewonly=True,
    )

    user_roles = db.relationship("UserHasEventRole", cascade="all, delete")

    daily_plans = db.relationship(
        "DailyPlan",
        back_populates="event",
        order_by=DailyPlan.date,
        cascade="all, delete",
    )

    attendees = db.relationship(
        "Attendee", primaryjoin="Attendee.event_id == Event.id", back_populates="event"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().set_defaults()

    def duplicate(self):
        event = Event()

        event.name = f"{self.name} (kopie)"
        event.date_from = self.date_from
        event.date_to = self.date_to

        event.people_count = self.people_count

        event.daily_plans = []

        event.save()

        for old_plan in self.daily_plans:
            plan = old_plan.duplicate()
            plan.event_id = event.id
            plan.edit()

        return event

    def toggle_archived(self):
        self.is_archived = not self.is_archived
        self.edit()
        return self.is_archived

    def toggle_shared(self):
        self.is_shared = not self.is_shared
        self.edit()
        return self.is_shared

    def share_all_used_recipes(self):
        for recipe in self.recipes:
            recipe.share()

    @property
    def relative_portion_count(self):
        relative_portion_count = 0

        # count portions of attendees with their portion size
        for attendee in self.attendees:
            relative_portion_count += attendee.portion_size_ratio

        # add remaining count
        relative_portion_count += self.people_count - len(self.attendees)

    @property
    def is_active(self) -> bool:
        return not self.is_archived

    @property
    def in_future(self) -> bool:
        return self.date_to >= datetime.date.today()

    @property
    def duration(self) -> int:
        return (self.date_to - self.date_from).days + 1

    @property
    def days(self) -> list:
        return [
            self.date_from + timedelta(days=x)
            for x in range((self.date_to - self.date_from).days + 1)
        ]

    def date_has_daily_plan(self, date) -> bool:
        return any(dp.date == date for dp in self.daily_plans)

    @property
    def active_daily_plans(self) -> list:
        return [
            dp for dp in self.daily_plans if (self.date_from <= dp.date <= self.date_to)
        ]

    @property
    def recipes(self) -> list:
        recipes = []
        for daily_plan in self.daily_plans:
            recipes += daily_plan.real_recipes

        return recipes

    @property
    def active_recipes(self) -> list:
        recipes = []
        for daily_plan in self.active_daily_plans:
            recipes += daily_plan.real_recipes

        return recipes

    @property
    def recipes_without_duplicated(self) -> list:
        return list_without_duplicated(self.recipes)

    @property
    def daily_recipes(self) -> list:
        daily_recipes = []
        for daily_plan in self.active_daily_plans:
            daily_recipes += daily_plan.daily_recipes

        return daily_recipes

    @property
    def daily_recipes_split_by_shopping(self) -> list:
        daily_recipes = self.daily_recipes
        split_recipes = []

        shopping_indexes = [0]
        for i, recipe in enumerate(daily_recipes):
            if recipe.is_shopping:
                shopping_indexes.append(i)

        shopping_indexes.append(len(daily_recipes))

        for i in range(len(shopping_indexes) - 1):
            i_from = shopping_indexes[i]
            i_to = shopping_indexes[i + 1]

            split_recipes.append(daily_recipes[i_from:i_to])

        return split_recipes

    @property
    def zero_amount_ingredient_recipes(self) -> list:
        return [r for r in self.active_recipes if r.has_zero_amount_ingredient]

    @property
    def no_measurement_ingredient_recipes(self) -> list:
        return [r for r in self.active_recipes if r.has_no_measurement_ingredient]

    @property
    def recipes_without_category(self) -> list:
        return [r for r in self.active_recipes if r.without_category]

    @property
    def no_category_ingredient_recipes(self) -> list:
        return [r for r in self.active_recipes if r.has_no_category_ingredient]

    @property
    def empty_recipes(self) -> list:
        return [r for r in self.active_recipes if r.is_draft]

    @property
    def starts_at(self):
        return self.date_from

    @property
    def ends_at(self):
        return self.date_to

    def user_role(self, user):
        roles = [user_role for user_role in self.user_roles if user_role.user == user]
        if not roles:
            return None
        elif len(roles) == 1:
            return roles[0].role
        else:
            raise Warning("User has multiple roles on this event")

    @property
    def connected_users(self) -> list:
        users = self.shared_with
        users.append(self.author)

        return users

    @property
    def other_user_ids(self) -> list:
        user_ids = [user.id for user in self.shared_with]
        user_ids.append(self.author.id)
        user_ids.remove(current_user.id)

        if len(user_ids) == 1:
            user_ids = user_ids[0]

        return user_ids

    @property
    def current_user_role(self):
        return self.user_role(current_user)

    # PERMISSIONS
    def can_view(self, user) -> bool:
        return (
            self.is_author(user)
            or self.user_role(user) in ["viewer", "collaborator"]
            or self.is_public
            or (user.is_authenticated and user.has_permission("see-other"))
        )

    def can_edit(self, user) -> bool:
        return (
            self.is_author(user)
            or self.user_role(user) == "collaborator"
            or (user.is_authenticated and user.has_permission("edit-other"))
        )

    def can_delete(self, user) -> bool:
        return self.is_author(user) or (
            user.is_authenticated and user.has_permission("edit-other")
        )

    def can_share(self, user) -> bool:
        return self.is_author(user) or (
            user.is_authenticated and user.has_permission("edit-other")
        )

    @property
    def can_current_user_share(self) -> bool:
        return self.can_share(current_user)
