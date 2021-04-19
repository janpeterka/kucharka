from datetime import datetime

from flask_security.models.fsqla_v2 import FsUserMixin as UserMixin
from flask_security.utils import hash_password

from app import db

from app.helpers.base_mixin import BaseMixin


class User(db.Model, BaseMixin, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime, default=datetime.now)

    roles = db.relationship(
        "Role",
        secondary="users_have_roles",
        backref=db.backref("users", lazy="dynamic"),
    )


def create(self):
    from app import user_datastore

    user_datastore.create_user(
        email=self.email,
        password=hash_password(self.password),
        name=self.name,
        nickname=self.nickname,
        choir_id=self.choir_id,
    )
    db.session.commit()

    # WIP return user object
