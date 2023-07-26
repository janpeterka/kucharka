from flask import url_for
from markupsafe import escape

from ..utils import classproperty

"""Mixin for automatically generating paths for object when using Flask-Classful (or similar)

Provides set of useful methods for getting paths to actions for a given object.
"""


class ClassfulLinkableMixin:
    VIEW_CLASS_SUFFIX = "View"

    @property
    def default_link_value(self) -> str:
        if hasattr(self, "name"):
            return escape(self.name)
        else:
            return escape(self.__str__)

    def path_to(self, action: str, **kwargs):
        if action == "new":
            return self.path_to_new(**kwargs)
        else:
            return url_for(f"{self._view_name}:{action}", id=self.id, **kwargs)

    @classmethod
    def path_to_new(cls, **kwargs):
        return url_for(f"{cls._class_view_name}:new", **kwargs)

    def path_to_show(self, **kwargs):
        return self.path_to("show", **kwargs)

    def path_to_edit(self, **kwargs):
        return self.path_to("edit", **kwargs)

    def path_to_update(self, **kwargs):
        return self.path_to("update", **kwargs)

    @property
    def url(self) -> str:
        return url_for(f"{self._view_name}:show", id=self.id)

    @property
    def url_to_update(self) -> str:
        return url_for(f"{self._view_name}:update", id=self.id)

    @property
    def external_url(self) -> str:
        return url_for(f"{self._view_name}:show", id=self.id, _external=True)

    # private

    @property
    def _view_name(self):
        return f"{type(self).__name__}{self.VIEW_CLASS_SUFFIX}"

    @classproperty
    def _class_view_name(cls):
        return f"{cls.__name__}{cls.VIEW_CLASS_SUFFIX}"
