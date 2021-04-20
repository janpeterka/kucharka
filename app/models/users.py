from datetime import datetime

from flask_security.models.fsqla_v2 import FsUserMixin as UserMixin

from app import db

from app.helpers.base_mixin import BaseMixin


class User(db.Model, BaseMixin, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    roles = db.relationship(
        "Role",
        secondary="users_have_roles",
        backref=db.backref("users", lazy="dynamic"),
    )

    daily_plans = db.relationship("DailyPlan", back_populates="author")
