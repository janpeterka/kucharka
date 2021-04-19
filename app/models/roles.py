from app import db
from flask_security import RoleMixin

from app.helpers.base_mixin import BaseMixin


class Role(db.Model, BaseMixin, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
