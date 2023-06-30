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
    obj_or_class=None,
    path=None,
    icon=None,
    value=None,
    confirmation=None,
    method=None,
    url=None,
    button_type=None,
    disabled=False,
    disabled_value=None,
    **kwargs,
):
    from app.components import icon as render_icon

    import inspect

    if inspect.isclass(obj_or_class):
        klass = obj_or_class
        obj = None
    else:
        klass = obj_or_class.__class__
        obj = obj_or_class

    if icon:
        icon_name = icon
    else:
        icon_name = None

    value_text = value

    if klass and action:
        if hasattr(klass, "link_info") and action in klass.link_info:
            if not method:
                method = klass.link_info[action].get("method", "GET")
            if not value_text:
                value_text = klass.link_info[action].get("value")
            confirmation_button_text = klass.link_info[action].get(
                "confirm-value", value_text
            )
            if not confirmation:
                confirmation = klass.link_info[action].get("confirmation", None)
            if not url:
                url = klass.link_info[action].get("url", None)
            if not button_type:
                button_type = klass.link_info[action].get(
                    "button_type", "secondary-action"
                )
            if not icon_name:
                icon_name = klass.link_info[action].get("icon", action)
        else:
            raise ValueError("Cannot decide on how to create action_badge.")
    else:
        value = value
        if not button_type:
            button_type = "secondary-action"
        confirmation_button_text = value_text

    if disabled and disabled_value:
        value_text = disabled_value

    icon = Markup(render_icon(icon_name))
    value = Markup(f'{icon} <span class="ms-1">{value_text}</span>')

    if not path:
        if url and obj:
            path = url_for(url, id=obj.id)
        elif url:
            path = url_for(url)
        elif obj is None:
            path = klass.path_to_new()
        else:
            path = obj.path_to(action)

    DEFAULT_CLASSES = "btn me-2 mb-2 mb-md-0 d-print-none"

    classes = (
        f"{DEFAULT_CLASSES} bg-color-{button_type} color-white {kwargs.pop('class','')}"
    )
    kwargs["class"] = classes

    if "data" not in kwargs:
        kwargs["data"] = {}

    kwargs["data"]["info-type"] = button_type.split("-")[1]
    kwargs["data"]["confirm-value"] = confirmation_button_text
    kwargs["data"]["disabled"] = disabled

    if method in ["POST"]:
        return pill_button_to(
            path, value, confirmation=confirmation, disabled=disabled, **kwargs
        )
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
    if type(obj_or_str) == str:
        path = _path_from_string(obj_or_str)
    else:
        path = obj_or_str.path_to_show()
    return path
