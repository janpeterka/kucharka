import factory

from app import db
from app.models import Recipe


class RecipeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Recipe
        sqlalchemy_session = db.session

    class Params:
        shared = factory.Trait(is_shared=True)

    name = factory.Sequence(lambda n: "Recipe %d" % n)
    created_by = 1
    portion_count = 1
    is_shared = False


class PublicRecipeFactory(RecipeFactory):
    is_shared = True
