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

    def __str__(self):
        return f"Day {self.date} of {self.event}"

    def __repr__(self):
        return f"Day {self.date} of {self.event}"

    def path_to_show(self):
        return None

    @property
    def default_link_value(self):
        return self.weekday

    @property
    def tasks(self):
        return []

    @property
    def daily_recipes(self):
        return []
