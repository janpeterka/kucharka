import os
from flask import get_flashed_messages

# import re
# import time

import datetime

from flask import request, redirect

# from flask import g

from flask_security import url_for_security

# from flask_security import current_user

from app import create_app

# from app import db


env = os.environ.get("APP_STATE", "default")
application = create_app(config_name=env)


@application.context_processor
def inject_globals():
    from app.data import template_data

    return dict(
        texts=template_data.texts,
    )


@application.context_processor
def utility_processor():
    def human_format_date(date, with_relative=True):
        formatted_date = date.strftime("%d.%m.%Y")

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

    def link_to(obj, text=None):
        if type(obj) == str:
            if obj == "login":
                if text is None:
                    text = "Přihlaste se"
                return f"<a href='{url_for_security('login')}'>{text}</a>"
            elif obj == "register":
                if text is None:
                    text = "Zaregistrujte se"
                return f"<a href='{url_for_security('register')}'>{text}</a>"
            else:
                raise NotImplementedError("This string has no associated link_to")

        try:
            return obj.link_to
        except Exception:
            raise NotImplementedError("This object link_to is probably not implemented")

    def list_of_links(array):
        html = "<ul>"
        for item in array:
            link_to_item = link_to(item)
            html += f"<li>{link_to_item}</li>"
        html += "</ul>"

        return html

    return dict(
        human_format_date=human_format_date,
        link_to=link_to,
        list_of_links=list_of_links,
    )


@application.before_request
def session_management():
    # current_user.logged_from_admin = session.get("logged_from_admin")

    if application.config["APP_STATE"] == "shutdown" and request.path not in [
        "/shutdown",
        "/static/css/style.css",
    ]:
        return redirect("/shutdown")
    elif request.path == "/shutdown" and application.config["APP_STATE"] != "shutdown":
        return redirect("/")


# @application.after_request
# def flash_if_turbo(response):
#     from app import turbo
#     from flask import render_template as template
#     from flask import session, get_flashed_messages

#     # if turbo
#     if response.headers["Content-Type"] == "text/vnd.turbo-stream.html; charset=utf-8":
#         messages = get_flashed_messages(with_categories=True)
#         session.pop("_flashes", None)

#         if messages:
#             flash_turbo_response = turbo.replace(
#                 template("base/_flashing.html.j2", messages=messages), target="flashing"
#             )
#             response.response.append(flash_turbo_response)

#     return response


@application.after_request
def flash_if_turbo(response):
    from app import turbo
    from flask import render_template as template
    from flask import session

    # try:
    #     print(type(response.response))
    #     print(response.response)
    # except:
    #     pass

    # if turbo
    if response.headers["Content-Type"] == "text/vnd.turbo-stream.html; charset=utf-8":
        print("turbo")
        messages = get_flashed_messages(with_categories=True)
        print(messages)

        session.pop("_flashes", None)
        print(get_flashed_messages())

        flash_turbo_response_empty = turbo.replace(
            template("base/_flashing.html.j2", messages=None), target="flashing"
        )

        print(flash_turbo_response_empty)

        response.response.append(flash_turbo_response_empty)

        # append turbo.replace(target="flashing")
        # if messages:
        #     flash_turbo_response = turbo.replace(
        #         template("base/_flashing.html.j2", messages=messages), target="flashing"
        #     )
        #     response.response.append(flash_turbo_response)
        # and empty flashing messages

    # try:
    #     print(type(response.response))
    #     print(response.response)
    # except:
    #     pass

    print(response.response)

    return response


# @application.before_request
# def log_request_start():
#     g.log_request_start_time = time.time()


# @application.teardown_request
# def log_request(exception=None):
#     from app.handlers.data import DataHandler
#     from app.models.request_log import RequestLog

#     if application.config["APP_STATE"] == "development":
#         return

#     db.session.expire_all()
#     pattern = re.compile("/static/")
#     if not pattern.search(request.path):
#         user_id = getattr(current_user, "id", None)

#         item_type = DataHandler.get_additional_request_data("item_type")
#         item_id = DataHandler.get_additional_request_data("item_id")

#         log = RequestLog(
#             url=request.path,
#             user_id=user_id,
#             remote_addr=request.environ["REMOTE_ADDR"],
#             item_type=item_type,
#             item_id=item_id,
#             duration=time.time() - g.log_request_start_time,
#         )
#         log.save()


# @application.shell_context_processor
# def make_shell_context():
#     return {"db": db, "User": User}
