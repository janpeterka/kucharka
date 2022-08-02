import factory

from app import db
from app.models import Ingredient


class IngredientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Ingredient
        sqlalchemy_session = db.session

    name = factory.Sequence(lambda n: "Ingredient %d" % n)
    created_by = 1
