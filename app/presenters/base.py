from app.helpers.general import classproperty

from flask_template_components.mixins import ClassfulLinkableMixin


class BasePresenter(ClassfulLinkableMixin):
    def __str__(self):
        if hasattr(self, "name"):
            return self.name
        else:
            return self.__str__

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
