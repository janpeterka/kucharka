from werkzeug.datastructures import MultiDict

from flask import session

from app.controllers.forms import *  # noqa: F401, F403


def create_form(form_class, **kwargs):
    """Creates form object from given class

    Creates form object based on multiple options.

    Primarily it gets data from session, if any were kept between redirects.
    Then it creates form object, filling it using data from session and/or given object

    Arguments:
        form_class {class} -- any form class, such as LoginForm, UserForm,..
        **kwargs {[kwarg]} -- array of keyword arguments

    Returns:
        form -- Form object, such as from LoginForm, UserForm,..
    """
    form_data = None
    if session.get("formdata") is not None:
        form_data = MultiDict(session.get("formdata"))
        session.pop("formdata")

    if form_data and "obj" in kwargs:
        form = form_class(form_data, obj=kwargs["obj"])
        form.validate()
    elif form_data:
        form = form_class(form_data)
        form.validate()
    elif "obj" in kwargs:
        # Fill with data from object
        form = form_class(obj=kwargs["obj"])
    else:
        form = form_class()

    return form


def save_form_to_session(form_data):
    """Saves form data to session

    Used to keep form data between redirects when form is not validated

    Arguments:
        form_data {request.form} -- request.form data
    """
    session["formdata"] = form_data
