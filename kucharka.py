import os

from app import create_app

env = os.getenv("APP_STATE", "default")
application = create_app(config_name=env)


@application.context_processor
def utility_processor():
    def human_format_date(date, with_weekday=True, with_relative=True):
        import datetime

        formatted_date = date.strftime("%d.%m.%Y")

        from app.helpers.formaters import week_day

        if with_weekday:
            formatted_date += f" ({week_day(date)})"

        if with_relative:
            if date == datetime.date.today():
                formatted_date += " - Dnes"
                # return "Dnes"
            elif date == datetime.date.today() + datetime.timedelta(days=-1):
                formatted_date += " - Včera"
                # return "Včera"
            elif date == datetime.date.today() + datetime.timedelta(days=1):
                formatted_date += " - Zítra"
                # return "Zítra"
            # else:
            # return date.strftime("%d.%m.%Y")

        return formatted_date

    def link_to(obj, link_type="show"):
        try:
            if link_type == "show":
                return obj.link_to
            elif link_type == "edit":
                return obj.link_to_edit

        except Exception:
            raise NotImplementedError(
                f"This object link_to (with {link_type}) is probably not implemented"
            )

    def formatted_amount(amount):
        import math

        if amount == 0:
            return 0

        if math.floor(amount) == 0:
            digits = 0
        else:
            digits = int(math.log10(math.floor(amount))) + 1

        if digits in [0, 1]:
            # if number is in ones, return with one decimal
            formatted_amount = round(amount, 1)
            # if first decimal is zero
            return (
                int(formatted_amount)
                if int(formatted_amount) == formatted_amount
                else formatted_amount
            )

        elif digits in (2, 3):
            # if number is in tens or hundereds, return without decimals
            return round(amount)

        return int(amount)

    return dict(
        human_format_date=human_format_date,
        link_to=link_to,
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

        if start_time := getattr(g, "log_request_start_time", None):
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
