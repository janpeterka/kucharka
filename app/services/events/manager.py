from app.models import DailyPlan


class EventManager:
    def __init__(self, event):
        self.event = event

    def add_new_daily_plans(self):
        for date in self.event.days:
            if not self.event.date_has_daily_plan(date):
                day_plan = DailyPlan(date=date, event=self.event)
                day_plan.save()
