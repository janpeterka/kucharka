import factory

from datetime import timedelta
from app import db
from app.models import Event


class EventFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Event
        sqlalchemy_session = db.session

    class Params:
        length = 12

    name = factory.Sequence(lambda n: "Event %d" % n)
    created_by = 1

    date_from = factory.Faker("date_time_this_year", before_now=False, after_now=True)
    date_to = factory.LazyAttribute(lambda o: o.date_from + timedelta(days=o.length))
