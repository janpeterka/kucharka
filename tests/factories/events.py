import factory

from datetime import timedelta
from app import db
from app.models import Event


class EventFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Event
        sqlalchemy_session = db.session
        exclude = ("datetime_begin", "datetime_end")

    # name = factory.Sequence(lambda n: "Event %d" % n)
    # created_by = 1


#     owned_by_group = 1
#     type_id = 1
#     datetime_begin = factory.Faker(
#         "date_time_this_year", before_now=False, after_now=True
#     )
#     datetime_end = factory.LazyAttribute(
#         lambda o: o.datetime_begin + timedelta(hours=2)
#     )
#     date_begin = factory.LazyAttribute(lambda o: o.datetime_begin.date())
#     time_begin = factory.LazyAttribute(lambda o: o.datetime_begin.time())
#     date_end = factory.LazyAttribute(lambda o: o.datetime_end.date())
#     time_end = factory.LazyAttribute(lambda o: o.datetime_end.time())


# class PastEventFactory(EventFactory):
#     datetime_begin = factory.Faker(
#         "date_time_this_year", before_now=True, after_now=False
#     )


# class FutureEventFactory(EventFactory):
#     datetime_begin = factory.Faker(
#         "date_time_this_year", before_now=False, after_now=True
#     )
