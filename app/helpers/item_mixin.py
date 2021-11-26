from app.helpers.base_mixin import BaseMixin


# Custom methods for all my classes
class ItemMixin(BaseMixin):
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
    def url(self):
        from flask import url_for

        self_view_name = f"{type(self).__name__}sView:show"
        return url_for(self_view_name, id=self.id)

    @property
    def link_to(self):
        from flask import url_for, Markup, escape

        self_view_name = f"{type(self).__name__}sView:show"
        return Markup(
            f"<a data-turbo='false' href='{url_for(self_view_name, id=self.id)}'> {escape(self.name)} </a>"
        )

    @property
    def link_to_edit(self):
        from flask import url_for, Markup, escape

        self_view_name = f"{type(self).__name__}sView:edit"

        return Markup(
            f"<a data-turbo='false' href='{url_for(self_view_name, id=self.id)}'> {escape(self.name)} </a>"
        )
