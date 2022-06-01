from flask import url_for, Markup, escape

from app.presenters import BasePresenter


class ItemPresenter(BasePresenter):
    @property
    def json(self):
        attributes = [a for a in self.__dict__.keys() if not a.startswith("_")]

        data = {}
        for attr in attributes:
            value = getattr(self, attr)
            if isinstance(value, list):
                data[attr] = ", ".join(str(x) for x in value)
            elif hasattr(value, "email"):
                data[attr] = value.email
            else:
                data[attr] = str(value)

        return data

    # CONTEXT PROCESSOR UTILITIES

    @property
    def _view_name(self):
        return f"{type(self).__name__}View"

    def _path_to_show(self, **kwargs):
        return url_for(f"{self._view_name}:show", id=self.id, **kwargs)

    def _path_to_edit(self, **kwargs):
        return url_for(f"{self._view_name}:edit", id=self.id, **kwargs)

    @property
    def _default_value(self):
        return escape(self.name)

    @property
    def url(self):
        return self._path_to_show()

    def link_to(self, value=None, **kwargs):
        if not value:
            value = self._default_value

        class_ = ""
        if "class" in kwargs:
            class_ = f"class=\"{kwargs['class']}\""

        return Markup(
            f"<a data-turbo='false' {class_} href='{self._path_to_show(**kwargs)}'>{value}</a>"
        )

    def link_to_edit(self, value=None, **kwargs):
        if not value:
            value = self._default_value

        class_ = ""
        if "class" in kwargs:
            class_ = f"class=\"{kwargs['class']}\""

        return Markup(
            f"<a data-turbo='false' {class_} href='{self._path_to_edit(**kwargs)}'>{value}</a>"
        )
