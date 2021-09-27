from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin


class LabelCategory(BaseModel, BaseMixin):
    __tablename__ = "label_categories"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
