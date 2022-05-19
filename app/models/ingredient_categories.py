from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin
from app.presenters import BasePresenter


class IngredientCategory(BaseModel, BaseMixin, BasePresenter):
    __tablename__ = "ingredient_categories"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    is_lasting = db.Column(db.Boolean, default=False)

    # PROPERTIES

    @property
    def is_used(self) -> bool:
        return bool(self.ingredients)

    @property
    def count(self) -> int:
        return len(self.ingredients)
