from flask import url_for, escape


class BasePresenter:
    def __str__(self):
        return self.name if hasattr(self, "name") else self.__str__

    @property
    def url(self) -> str:
        return url_for(f"{self._view_name}:show", id=self.id)

    @property
    def url_to_update(self) -> str:
        return url_for(f"{self._view_name}:update", id=self.id)

    @property
    def external_url(self) -> str:
        return url_for(f"{self._view_name}:show", id=self.id, _external=True)

    @property
    def _view_name(self):
        return f"{type(self).__name__}View"

    @property
    def default_link_value(self):
        return escape(self.name)

    def path_to(self, action, **kwargs):
        if action == "show":
            return self.path_to_show(**kwargs)
        elif action == "edit":
            return self.path_to_edit(**kwargs)

        else:
            return url_for(f"{self._view_name}:{action}", id=self.id, **kwargs)

    def path_to_show(self, **kwargs):
        return url_for(f"{self._view_name}:show", id=self.id, **kwargs)

    def path_to_edit(self, **kwargs):
        return url_for(f"{self._view_name}:edit", id=self.id, **kwargs)

    def path_to_update(self, **kwargs):
        return url_for(f"{self._view_name}:update", id=self.id, **kwargs)
