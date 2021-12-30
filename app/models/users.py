from flask_security.models.fsqla_v2 import FsUserMixin as UserMixin
from flask_security import hash_password

from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin

from app.modules.calendar.models.calendar_user_mixin import CalendarUserMixin


class User(BaseModel, BaseMixin, UserMixin, CalendarUserMixin):
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
        return User.load_by_attribute("username", username)

    # PROPERTIES

    @property
    def name(self):
        if self.full_name:
            return self.full_name
        else:
            return ""

    @property
    def has_password(self):
        return self.password != "x"

    @property
    def active_events(self):
        return [e for e in self.events if e.is_active]

    @property
    def active_future_events(self):
        return [e for e in self.active_events if e.in_future]

    @property
    def closest_future_event(self):
        if not self.active_future_events:
            return None

        closest_event = self.active_future_events[0]
        for event in self.active_future_events:
            if event.date_from > closest_event.date_from:
                closest_event = event

        return closest_event

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

    # ROLES
    # @property
    # def is_admin(self):
    #     # from flask import session

    #     return self.has_role("admin")
    #     # return self.has_role("admin") and not session.get("as_commoner", False)

    # @property
    # def is_application_manager(self):
    #     return self.has_role("application_manager")
