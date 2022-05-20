from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin
from app.presenters import BasePresenter


class LabelCategory(BaseModel, BaseMixin, BasePresenter):
    __tablename__ = "label_categories"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    allow_multiple = db.Column(db.Boolean, default=True)
