import os

from app import create_app, cli

env = os.getenv("APP_STATE", "default")
application = create_app(config_name=env)

cli.register(application)


@application.context_processor
def context_processors():
    from app.helpers.context_processors import (
        human_format_date,
        link_to,
        link_to_edit,
        formatted_amount,
        inflect,
    )

    return dict(
        human_format_date=human_format_date,
        formatted_amount=formatted_amount,
        link_to=link_to,
        link_to_edit=link_to_edit,
        inflect=inflect,
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
