import factory

from app import db
from app.models import RecipeTask


class RecipeTaskFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = RecipeTask
        sqlalchemy_session = db.session

    name = factory.Sequence(lambda n: "Recipe task %d" % n)
    description = "Do something"
    days_before_cooking = 1
