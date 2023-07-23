from flask import url_for
from markupsafe import Markup
from app.packages.template_components import BaseComponent


# core
class Link(BaseComponent):
    def __init__(self, path, value, **kwargs):
        super(Link, self).__init__(**kwargs)
        self.path = path
        self.value = value


class ButtonLink(Link):
    folder = "links"
    file = "link"

    def __init__(self, path, value, **kwargs):
        super(ButtonLink, self).__init__(path, value, **kwargs)
        self.kwargs["class"] = (
            self.kwargs.get("class", "") + f" btn btn-{kwargs.get('button_type')}"
        )


# helpers
def link_to(obj_or_str, turbo=True, **kwargs):
    path = _get_path(obj_or_str)

    value = kwargs.pop("value", None)
    if not value:
        value = obj_or_str.default_link_value

    if turbo is False:
        kwargs["data"] = kwargs.get("data", {})
        kwargs["data"]["turbo-frame"] = "_top"

    return Link(path=path, value=value, **kwargs).render()


def link_to_edit(obj, **kwargs):
    from app.components import icon

    path = obj.path_to_edit()

    if kwargs.get("value", None) is None:
        kwargs["value"] = f"{obj.name} " + Markup(icon("edit"))

    return Link(path=path, **kwargs).render()


# internal


def _path_from_string(text):
    if ":" in text:
        text = url_for(text)

    return text


def _get_path(obj_or_str):
    if type(obj_or_str) == str:
        path = _path_from_string(obj_or_str)
    else:
        path = obj_or_str.path_to_show()
    return path
