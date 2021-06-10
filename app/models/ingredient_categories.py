from unidecode import unidecode

from app import db

from app.helpers.base_mixin import BaseMixin


class IngredientCategory(db.Model, BaseMixin):
    __tablename__ = "ingredient_categories"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    is_lasting = db.Column(db.Boolean, default=False)

    # LOADERS
    @staticmethod
    def load_all(ordered=True):
        categories = IngredientCategory.query.all()

        if ordered:
            categories.sort(key=lambda x: unidecode(x.name.lower()))

        return categories

    # PROPERTIES

    @property
    def is_used(self) -> bool:
        return True if self.ingredients else False
