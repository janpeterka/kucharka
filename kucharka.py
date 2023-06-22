import os

from app import create_app, cli

env = os.getenv("APP_STATE", "default")
application = create_app(config_name=env)

cli.register(application)


@application.context_processor
def context_processors():
    from app.helpers.context_processors import context_processors
    from app.models import all_dict as models
    from app.forms import IngredientForm, RecipeIngredientForm

    return dict(
        **context_processors,
        **models,
        IngredientForm=IngredientForm,
        RecipeIngredientForm=RecipeIngredientForm,
    )


@application.before_request
def session_management():
    from flask import request, redirect

    if application.config["APP_STATE"] == "shutdown" and request.path not in [
        "/shutdown",
        "/static/css/style.css",
    ]:
        return redirect("/shutdown")
    elif request.path == "/shutdown" and application.config["APP_STATE"] != "shutdown":
        return redirect("/")


@application.before_request
def set_feature_flags():
    from flask import request

    if not (request.path.endswith("css") or request.path.endswith("js")):
        for arg, value in request.args.to_dict().items():
            if arg.startswith("ff_"):
                application.config[arg.upper()] = bool(int(value))


@application.before_request
def sentry_add_user():
    from sentry_sdk import set_user
    from flask_security import current_user

    if current_user.is_authenticated:
        set_user({"id": current_user.id, "username": current_user.name_or_email})


@application.after_request
def after_request(response):
    from flask import render_template
    from app import turbo

    # if the response has the turbo-stream content type, then append one more
    # stream with the contents of the alert section of the page
    if response.headers["Content-Type"].startswith("text/vnd.turbo-stream.html"):
        response.response.append(
            turbo.update(render_template("base/_flashing.html.j2"), "flashes").encode()
        )
        if response.content_length:
            response.content_length += len(response.response[-1])
    return response
