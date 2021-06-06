from datetime import datetime

from flask_security.models.fsqla_v2 import FsUserMixin as UserMixin

from app import db

from app.helpers.base_mixin import BaseMixin


class User(db.Model, BaseMixin, UserMixin):
    from app.models.users_have_roles import users_have_roles

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    full_name = db.Column(db.String(255))

    roles = db.relationship("Role", secondary="users_have_roles", backref="users")

    daily_plans = db.relationship("DailyPlan", back_populates="author")

    # PROPERTIES

    @property
    def is_admin(self):
        return self.has_role("admin")

    @property
    def is_application_manager(self):
        return self.has_role("application_manager")

    @property
    def name(self):
        return self.full_name

    @property
    def visible_recipes(self):
        return [r for r in self.recipes if r.is_visible]

    @property
    def draft_recipes(self):
        return [r for r in self.recipes if r.is_draft]
