from app import db

from app.helpers.base_mixin import BaseMixin


class RecipeCategory(db.Model, BaseMixin):
    __tablename__ = "recipe_categories"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # PROPERTIES

    @property
    def is_used(self) -> bool:
        return bool(self.recipes)
