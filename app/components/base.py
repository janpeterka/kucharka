from flask import render_template as render
from flask import Markup


class BaseComponent:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.kwargs["data"] = self.kwargs.pop("data", {})

    def render(self, remove_newlines=True):
        html = render(self.template, **self.attributes)
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
    def template(self):
        folder = getattr(self, "folder", f"{self.__class__.__name__.lower()}s")
        file = getattr(self, "file", f"{self.__class__.__name__.lower()}")

        return f"components/{folder}/{file}.html.j2"

    @property
    def attributes(self):
        # All public variables of the view are passed to template
        class_attributes = self.__class__.__dict__
        view_attributes = self.__dict__
        all_attributes = class_attributes | view_attributes
        public_attributes = {
            k: all_attributes[k] for k in all_attributes if not k.startswith("_")
        }

        return {**public_attributes, **self.kwargs}
