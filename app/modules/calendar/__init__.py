from .calendar import generate_ical, generate_ical_response  # noqa F401


def create_module(app, **kwargs):
    from .calendar import calendar_blueprint

    app.register_blueprint(calendar_blueprint)
