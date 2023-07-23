from flask import render_template
from markupsafe import Markup


class BaseComponent:
    """Base class for all TemplateComponents.

    provides `render` method, which renders template with attributes passed to it.

    :param DEFAULT_CLASSES: list of css classes to be added to the component
    :type DEFAULT_CLASSES: list
    :param folder: folder to look for template in, defaults to component class name in lowercase
    :type folder: str
    :param file: template file name to render, defaults to component class name in lowercase
    :type file: str
    """

    DEFAULT_CLASSES = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.kwargs["data"] = self.kwargs.pop("data", {})

    def render(self, remove_newlines=True):
        html = render_template(self._template, **self._attributes)
        if remove_newlines:
            html = html.replace("\n", "")
        while "  " in html:
            html = html.replace("  ", " ")
        html = html.replace(" >", ">")
        html = html.replace("> <", "><")
        html = html.replace('=" ', '="')
        html = html.replace(' "', '"')
        html = html.strip()

        return Markup(html)

    @property
    def _template(self):
        folder = getattr(self, "folder", f"{self.__class__.__name__.lower()}s")
        file = getattr(self, "file", f"{self.__class__.__name__.lower()}")

        # WIP: how to select default templates from package, not from project templates?
        return f"components/{folder}/{file}.html.j2"

    @property
    def _attributes(self):
        # All public variables of the view are passed to template
        class_attributes = self.__class__.__dict__
        view_attributes = self.__dict__
        all_attributes = class_attributes | view_attributes
        public_attributes = {
            k: all_attributes[k] for k in all_attributes if not k.startswith("_")
        }

        # kwargs has higher priority, therefore rewrites public attributes
        merged_values = {**public_attributes, **self.kwargs}
        return merged_values
