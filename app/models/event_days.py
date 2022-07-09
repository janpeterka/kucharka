from .mixins.day_mixin import DayMixin


class EventDay(DayMixin):
    def __init__(self, date=None, event=None, *args, **kwargs):
        from app.helpers.formaters import week_day

        if date is None:
            raise AttributeError("EventDay needs date!")
        if event is None:
            raise AttributeError("EventDay needs event!")

        self.event = event
        self.date = date
        self.weekday = week_day(self.date)

    def link_to(self):
        return self.weekday

    @property
    def tasks(self):
        return []

    @property
    def daily_recipes(self):
        return []
