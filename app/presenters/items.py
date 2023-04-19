from flask import url_for, escape

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
