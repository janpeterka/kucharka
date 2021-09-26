from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin


class Label(BaseModel, BaseMixin):
    __tablename__ = "labels"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    category_id = db.Column(db.ForeignKey("label_categories.id"))
    category = db.relationship("LabelCategory", uselist=False, backref="labels")
