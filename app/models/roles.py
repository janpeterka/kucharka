from app import db, BaseModel
from flask_security import RoleMixin

from app.helpers.base_mixin import BaseMixin


class Role(BaseModel, BaseMixin, RoleMixin):
    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
