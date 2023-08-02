from flask_template_components import BaseComponent


class DayCard(BaseComponent):
    # WIP: There is problem with FlaskTemplateComponents, DEFAULT_CLASSES are overridden instead of appended
    # DEFAULT_CLASSES = [
    #     "col-12",
    #     "col-md",
    #     "p-2",
    #     "mb-2",
    #     "mb-md-3",
    #     "ms-2",
    #     "me-2",
    #     "rounded",
    #     "text-center",
    #     "text-nobreak",
    # ]

    def __init__(self, day, **kwargs):
        super().__init__(**kwargs)
        self.day = day
        self.event = day.event


class ActiveDayCard(DayCard):
    DEFAULT_CLASSES = [
        "clickable",
        "col-12",
        "col-md",
        "p-2",
        "mb-2",
        "mb-md-3",
        "ms-2",
        "me-2",
        "rounded",
        "text-center",
        "text-nobreak",
    ]

    def __init__(self, day, **kwargs):
        super().__init__(day, **kwargs)

        self.color = "secondary"


class InactiveDayCard(DayCard):
    DEFAULT_CLASSES = [
        "opacity-50",
        "d-none",
        "d-md-inline-block",
        "cursor-default",
        "col-12",
        "col-md",
        "p-2",
        "mb-2",
        "mb-md-3",
        "ms-2",
        "me-2",
        "rounded",
        "text-center",
        "text-nobreak",
    ]

    def __init__(self, day, **kwargs):
        super().__init__(day, **kwargs)

        self.color = "light-grey"


def day_card(day, **kwargs):
    if day.is_active:
        return ActiveDayCard(day, **kwargs).render()
    else:
        return InactiveDayCard(day, **kwargs).render()
