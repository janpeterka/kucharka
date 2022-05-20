from app.presenters import ItemPresenter


class DailyPlanPresenter(ItemPresenter):
    @property
    def week(self) -> int:
        return int(self.date.strftime("%V"))

    @property
    def name(self) -> str:
        return self.weekday

    @property
    def weekday(self) -> str:
        from app.helpers.formaters import week_day

        return week_day(self.date)
