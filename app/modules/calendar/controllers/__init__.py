from .calendar import CalendarView

__all__ = ["CalendarView"]


def register_all_controllers(application):
    CalendarView.register(application)
