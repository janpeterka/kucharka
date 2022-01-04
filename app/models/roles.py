from app import db, BaseModel

# from flask_security import RoleMixin
from flask_security.models.fsqla_v2 import FsRoleMixin as RoleMixin

from app.helpers.base_mixin import BaseMixin


class Role(BaseModel, BaseMixin, RoleMixin):
    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)  # type: ignore
    name = db.Column(db.String(80), unique=True)  # type: ignore
    description = db.Column(db.String(255))  # type: ignore
