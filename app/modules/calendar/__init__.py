def create_module(app, **kwargs):
    from .controllers.calendar import calendar_blueprint

    app.register_blueprint(calendar_blueprint)

    from .controllers import register_all_controllers  # noqa: F401

    register_all_controllers(app)
