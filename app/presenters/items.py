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

    @property
    def _show_path(self):
        return url_for(f"{self._view_name}:show", id=self.id)

    @property
    def _edit_path(self):
        return url_for(f"{self._view_name}:edit", id=self.id)

    @property
    def url(self):
        from flask import url_for

        return url_for(f"{self._view_name}:show", id=self.id)

    @property
    def link_to(self):
        return Markup(
            f"<a data-turbo='false' href='{self._show_path}'>{escape(self.name)}</a>"
        )

    @property
    def link_to_edit(self):
        return Markup(
            f"<a data-turbo='false' href='{self._edit_path}'>{escape(self.name)}</a>"
        )
