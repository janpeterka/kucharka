from flask import Blueprint

bp = Blueprint("template_components", __name__, template_folder="templates")


class TemplateComponents:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.register_blueprint(bp)
