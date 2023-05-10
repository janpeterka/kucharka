from werkzeug.datastructures import MultiDict
from flask import session

from app.forms import *  # noqa: F401, F403

# from wtforms.widgets import html_params


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


def load_from_form_to_object(obj, *, form, attributes: list):
    for attribute in attributes:
        form_data = getattr(form, attribute).data
        setattr(obj, attribute, form_data)


# class ExtendedSelectWidget:
#     """
#     Renders a select field allowing custom attributes for options.
#     Expects the field to be an iterable object of Option fields.
#     The render function accepts a dictionary of option ids ("{field_id}-{option_index}")
#     which contain a dictionary of attributes to be passed to the option.

#     Example:
#     form.customselect(option_attr={"customselect-0": {"disabled": ""} })
#     """

#     def __init__(self, multiple=False):
#         self.multiple = multiple

#     def __call__(self, field, option_attr=None, **kwargs):
#         if option_attr is None:
#             option_attr = {}
#         kwargs.setdefault("id", field.id)
#         if self.multiple:
#             kwargs["multiple"] = True
#         if "required" not in kwargs and "required" in getattr(field, "flags", []):
#             kwargs["required"] = True
#         html = ["<select %s>" % html_params(name=field.name, **kwargs)]
#         for option in field:
#             attr = option_attr.get(option.id, {})
#             html.append(option(**attr))
#         html.append("</select>")
#         return Markup("".join(html))
