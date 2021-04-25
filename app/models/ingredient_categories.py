from app import db

from app.helpers.base_mixin import BaseMixin


class IngredientCategory(db.Model, BaseMixin):
    __tablename__ = "ingredient_categories"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
