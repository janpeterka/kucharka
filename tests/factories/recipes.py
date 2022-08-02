import factory

from app import db
from app.models import Recipe


class RecipeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Recipe
        sqlalchemy_session = db.session

    name = factory.Sequence(lambda n: "Recipe %d" % n)
    created_by = 1
