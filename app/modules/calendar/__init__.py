from .calendar import generate_ical  # noqa F401


def create_module(app, **kwargs):
    from .calendar import calendar_blueprint

    app.register_blueprint(calendar_blueprint)
