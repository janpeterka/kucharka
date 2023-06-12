from flask import url_for
from markupsafe import Markup
from app.components.buttons import ButtonTo
from app.components.links import Link


class PillLink(Link):
    folder = "links"
    file = "link"

    def __init__(self, path, value, **kwargs):
        super(PillLink, self).__init__(path, value, **kwargs)


def action_badge(  # noqa: C901
    action=None,
    obj=None,
    path=None,
    icon=None,
    value=None,
    confirmation=None,
    method="GET",
    url=None,
    button_type="outline-primary",
    **kwargs,
):
    from app.components import icon as render_icon

    # if not klass and obj:
    #     klass = obj.__class__
    #     while klass.__name__ not in VALUES and klass.__bases__:
    #         klass = klass.__bases__[0]

    #     klass = klass.__name__
    # else:
    #     klass = None

    icon_name = icon if icon else None
    if obj and action:
        if not hasattr(obj, "link_info") or action not in obj.link_info:
            raise ValueError("Cannot decide on how to create action_badge.")
        method = obj.link_info[action].get("method", method)
        value_text = obj.link_info[action].get("value", value)
        confirmation = obj.link_info[action].get("confirmation", confirmation)
        url = obj.link_info[action].get("url", url)
        button_type = obj.link_info[action].get("button_type", button_type)
        if not path:
            path = obj.link_info[action].get("path", None)
        if not icon_name:
            icon_name = obj.link_info[action].get("icon", action)
    else:
        value_text = value

    icon = Markup(render_icon(icon_name))
    value = Markup(f"{icon} {value_text}")
    if not path:
        path = url_for(url, id=obj.id) if url else obj.path_to(action)
    kwargs[
        "class"
    ] = f"btn bg-color-{button_type} color-white ps-2 pe-2 p-1 me-2 mb-2 mb-md-0 d-print-none {kwargs.pop('class','')}"

    if method in ["POST"]:
        return pill_button_to(path, value, confirmation=confirmation, **kwargs)
    else:
        return pill_link_to(path, value, **kwargs)


def pill_button_to(path, value, **kwargs):
    kwargs["form_class"] = f"d-inline-block {kwargs.pop('form_class','')}"

    return ButtonTo(path, value, **kwargs).render()


def pill_link_to(path, value=None, **kwargs):
    return PillLink(path=path, value=value, **kwargs).render()


def pill_link_to_edit(obj_or_str, button_type="primary", **kwargs):
    from app.components import icon

    path = _get_path(obj_or_str)

    if kwargs.get("value", None) is None:
        kwargs["value"] = icon("edit")

    return PillLink(
        path=path, value=kwargs.pop("value"), button_type=button_type, **kwargs
    ).render()


# internal


def _path_from_string(text):
    if ":" in text:
        text = url_for(text)

    return text


def _get_path(obj_or_str):
    return (
        _path_from_string(obj_or_str)
        if type(obj_or_str) == str
        else obj_or_str.path_to_show()
    )
