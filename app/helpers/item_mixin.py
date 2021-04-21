# from sqlalchemy import and_
# from flask_login import current_user

from app.helpers.base_mixin import BaseMixin

# from app.models.request_log import RequestLog


# Custom methods for all my classes
class ItemMixin(BaseMixin):
    @property
    def json(self):
        attributes = [a for a in self.__dict__.keys() if not a.startswith("_")]

        data = {}
        for attr in attributes:
            value = getattr(self, attr)
            if isinstance(value, list):
                data[attr] = ", ".join([str(x) for x in value])
            elif hasattr(value, "email"):
                data[attr] = value.email
            # elif hasattr[value, "measurement"]:
                # data[attr] = value.name
            else:
                data[attr] = str(value)

        return data

    # @property
    # def view_count(self) -> int:
    #     log_count = RequestLog.query.filter(
    #         and_(
    #             RequestLog.item_id == self.id,
    #             RequestLog.item_type == self.__class__.__name__.lower(),
    #             RequestLog.user_id == getattr(current_user, "id", None),
    #         )
    #     ).count()
    #     return log_count

    # CONTEXT PROCESSOR UTILITIES
    @property
    def link_to(self):
        from flask import url_for

        self_view_name = f"{type(self).__name__.capitalize()}sView:show"
        return f"<a href='{url_for(self_view_name, id=self.id)}'>{self.name}</a>"
