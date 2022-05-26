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

    def _show_path(self, **kwargs):
        return url_for(f"{self._view_name}:show", id=self.id, **kwargs)

    def _edit_path(self, **kwargs):
        return url_for(f"{self._view_name}:edit", id=self.id, **kwargs)

    @property
    def url(self):
        from flask import url_for

        return url_for(f"{self._view_name}:show", id=self.id)

    def link_to(self, **kwargs):
        return Markup(
            f"<a data-turbo='false' href='{self._show_path(**kwargs)}'>{escape(self.name)}</a>"
        )

    def link_to_edit(self, **kwargs):
        return Markup(
            f"<a data-turbo='false' href='{self._edit_path(**kwargs)}'>{escape(self.name)}</a>"
        )
