import os

from app import create_app

env = os.getenv("APP_STATE", "default")
application = create_app(config_name=env)


@application.context_processor
def utility_processor():
    from app.helpers.context_processors import (
        human_format_date,
        link_to,
        link_to_edit,
        formatted_amount,
    )

    return dict(
        human_format_date=human_format_date,
        link_to=link_to,
        link_to_edit=link_to_edit,
        formatted_amount=formatted_amount,
    )


@application.before_request
def session_management():
    from flask import request, redirect

    # current_user.logged_from_admin = session.get("logged_from_admin")

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


@application.before_request
def log_request_start():
    from flask import g
    import time

    g.log_request_start_time = time.time()


@application.teardown_request
def log_request(exception=None):
    import re
    import time
    from flask import request, g
    from flask_security import current_user
    from app import db
    from app.handlers.data import DataHandler
    from app.models.request_logs import RequestLog

    db.session.expire_all()

    ignore_pattern = re.compile("/static/")

    if not ignore_pattern.search(request.path):
        user_id = getattr(current_user, "id", None)
        item_type = DataHandler.get_additional_request_data("item_type")
        item_id = DataHandler.get_additional_request_data("item_id")

        start_time = getattr(g, "log_request_start_time", None)
        if start_time:
            duration = time.time() - start_time
        else:
            duration = None

        log = RequestLog(
            url=request.path,
            user_id=user_id,
            remote_addr=request.environ.get("REMOTE_ADDR", None),
            item_type=item_type,
            item_id=item_id,
            duration=duration,
        )
        log.save()
