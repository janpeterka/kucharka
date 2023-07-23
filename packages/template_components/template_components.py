from flask import Blueprint

bp = Blueprint("template_components", __name__, template_folder="templates")


class TemplateComponents:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.register_blueprint(bp)

        @app.context_processor
        def utility_processor():
            from markupsafe import Markup

            def render_class(classes: str):
                if not classes:
                    return ""

                return Markup(f'class="{classes}"')

            def render_data(data: dict):
                if not data:
                    return ""

                return Markup(" ".join([f"data-{k}='{v}'" for k, v in data.items()]))

            return dict(render_class=render_class, render_data=render_data)
