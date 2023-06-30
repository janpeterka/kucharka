from flask import url_for
from markupsafe import escape

from app.helpers.general import classproperty


class BasePresenter:
    def __str__(self):
        if hasattr(self, "name"):
            return self.name
        else:
            return self.__str__

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

    @classproperty
    def _class_view_name(cls):
        return f"{cls.__name__}View"

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

    @classmethod
    def path_to_new(cls, **kwargs):
        return url_for(f"{cls._class_view_name}:new", **kwargs)

    # action_badges
    @classproperty
    def link_info(self):
        from .common.links import DEFAULT_LINK_INFO

        if not hasattr(self, "LINK_INFO"):
            return DEFAULT_LINK_INFO

        NEW_LINK_INFO = {}

        # merge values from presenter and defaults
        for key, values in self.LINK_INFO.items():
            NEW_LINK_INFO[key] = {**DEFAULT_LINK_INFO.get(key, {}), **values}

        # add values from defaults that are not in presenter
        for key, values in DEFAULT_LINK_INFO.items():
            if key not in self.LINK_INFO:
                NEW_LINK_INFO[key] = values

        return NEW_LINK_INFO
