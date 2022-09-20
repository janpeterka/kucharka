from operator import attrgetter

from flask_security.models.fsqla_v2 import FsUserMixin as UserMixin
from flask_security import hash_password

from app import db, BaseModel, turbo
from app.helpers.general import flatten

from app.helpers.base_mixin import BaseMixin
from app.presenters import BasePresenter

from app.modules.calendar.models.calendar_user_mixin import CalendarUserMixin


class User(BaseModel, BaseMixin, UserMixin, CalendarUserMixin, BasePresenter):
    from app.models.users_have_roles import users_have_roles

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)  # type: ignore
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # type: ignore
    full_name = db.Column(db.String(255))  # type: ignore

    roles = db.relationship("Role", secondary="users_have_roles", backref="users")  # type: ignore

    daily_plans = db.relationship("DailyPlan", back_populates="author")  # type: ignore

    recipes = db.relationship("Recipe", order_by="Recipe.name", back_populates="author")  # type: ignore

    events = db.relationship("Event", back_populates="author")  # type: ignore

    role_events = db.relationship(
        "Event",
        secondary="users_have_event_roles",
        primaryjoin="User.id == UserHasEventRole.user_id",
        viewonly=True,
    )

    portion_types = db.relationship(
        "PortionType",
        primaryjoin="PortionType.created_by == User.id",
        back_populates="author",
    )

    @staticmethod
    def create(email, password, do_hash=True, **kwargs):
        from app import user_datastore

        if do_hash:
            password = hash_password(password)

        return user_datastore.create_user(email=email, password=password, **kwargs)

    def set_password(self, password):
        self.password = hash_password(password)

    # LOADERS

    @staticmethod
    def load_by_username(username):
        return User.load_by(username=username)

    # PROPERTIES

    @property
    def name(self) -> str:
        return self.full_name or ""

    @property
    def name_or_email(self) -> str:
        return self.full_name or self.email

    @property
    def has_password(self) -> bool:
        return self.password != "x"

    @property
    def all_events(self) -> list:
        return self.events + self.role_events

    @property
    def active_events(self) -> list:
        return [e for e in self.events if e.is_active]

    @property
    def all_active_events(self) -> list:
        return [e for e in self.all_events if e.is_active]

    @property
    def active_future_events(self) -> list:
        return [e for e in self.active_events if e.in_future]

    @property
    def all_active_future_events(self) -> list:
        return [e for e in self.all_active_events if e.in_future]

    @property
    def closest_future_event(self):
        if not self.active_future_events:
            return None

        return min(self.active_future_events, key=attrgetter("date_from"))

    @property
    def all_closest_future_event(self):
        if not self.all_active_future_events:
            return None

        return min(self.all_active_future_events, key=attrgetter("date_from"))

    @property
    def archived_events(self):
        return [e for e in self.events if e.is_archived]

    @property
    def visible_recipes(self):
        return [r for r in self.recipes if r.is_visible]

    @property
    def draft_recipes(self):
        return [r for r in self.recipes if r.is_draft]

    @property
    def recipes_with_zero_amount(self):
        return [r for r in self.recipes if r.has_zero_amount_ingredient]

    @property
    def recipes_without_category(self):
        return [r for r in self.recipes if r.without_category]

    @property
    def personal_ingredients(self):
        return [i for i in self.ingredients if not i.is_public]

    @property
    def ingredients_without_category(self):
        return [i for i in self.personal_ingredients if i.without_category]

    @property
    def ingredients_without_measurement(self):
        return [i for i in self.personal_ingredients if i.without_measurement]

    @property
    def role_event_recipes(self):
        recipes = [event.recipes for event in self.role_events]
        return flatten(recipes)

    @turbo.user_id
    def get_user_id():
        from flask_security import current_user

        if not current_user.is_authenticated:
            return None

        return current_user.id

    # ROLES
    # @property
    # def is_admin(self):
    #     # from flask import session

    #     return self.has_role("admin")
    #     # return self.has_role("admin") and not session.get("as_commoner", False)

    # @property
    # def is_application_manager(self):
    #     return self.has_role("application_manager")
