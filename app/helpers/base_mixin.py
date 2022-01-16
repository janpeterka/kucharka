import datetime

from flask import current_app as application

from flask_security import current_user

from sqlalchemy.sql import func

from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.hybrid import hybrid_property

from app import db


# Custom methods for all my classes
class BaseMixin(object):
    def __str__(self):
        return self.name if hasattr(self, "name") else self.__str__

    def set_defaults(self, **kwargs):
        if self.created_by is None:
            self.created_by = current_user.id

    def fill(self, form):
        form.populate_obj(self)

    # LOADERS

    @classmethod
    def load(cls, *args, **kwargs):
        object_id = kwargs.get("id", args[0])
        return cls.query.filter_by(id=object_id).first()

    @classmethod
    def load_all(cls, ordered_by_name=True):
        from unidecode import unidecode

        objects = cls.query.all()

        if ordered_by_name and hasattr(cls, "name"):
            objects.sort(key=lambda x: unidecode(x.name.lower()))

        return objects

    @classmethod
    def load_last(cls):
        return cls.query.all()[-1]

    @classmethod
    def load_all_by_name(cls, name):
        return cls.query.filter_by(name=name).all()

    @classmethod
    def load_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def load_all_by_attribute(cls, attribute, value):
        if not hasattr(cls, attribute):
            raise AttributeError

        return cls.query.filter_by(**{attribute: value}).all()

    @classmethod
    def load_by_attribute(cls, attribute, value):
        elements = cls.load_all_by_attribute(attribute, value)
        return elements[0] if elements else None

    # OTHER LOADING
    @classmethod
    def created_at_date(cls, date):
        if hasattr(cls, "created_at"):
            attr = "created_at"
        else:
            raise AttributeError('No "created_at" for created_recently')

        return cls.query.filter(func.DATE(getattr(cls, attr)) == date).all()

    @classmethod
    def created_recently(cls, days=30):
        date_from = datetime.date.today() - datetime.timedelta(days=days)
        if hasattr(cls, "created_at"):
            attr = "created_at"
        else:
            raise AttributeError('No "created_at" for created_recently')

        return cls.query.filter(getattr(cls, attr) > date_from).all()

    @classmethod
    def created_in_last_30_days(cls):
        return cls.created_recently(days=30)

    # DATABASE OPERATIONS

    def edit(self, **kw):
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            application.logger.error("Edit error: {}".format(e))
            return False

    def save(self, **kw):
        """Saves (new) object"""
        try:
            db.session.add(self)
            db.session.commit()
            if hasattr(self, "id"):
                return self.id is not None
        except DatabaseError as e:
            db.session.rollback()
            application.logger.error("Save error: {}".format(e))
            return False

    def remove(self, **kw):
        """Deletes object"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except DatabaseError as e:
            db.session.rollback()
            application.logger.error("Remove error: {}".format(e))
            return False

    def delete(self, **kw):
        return self.remove(**kw)

    def expire(self, **kw):
        """Dumps database changes"""
        try:
            db.session.expire(self)
            return True
        except Exception as e:
            db.session.rollback()
            application.logger.error("Expire error: {}".format(e))
            return False

    def refresh(self, **kw):
        try:
            db.session.refresh(self)
            return True
        except Exception as e:
            db.session.rollback()
            application.logger.error("Refresh error: {}".format(e))
            return False

    def reload(self):
        return type(self).load(self.id)

    # PROPERTIES

    def is_author(self, user) -> bool:
        return self.author == user if hasattr(self, "author") else False

    @property
    def is_current_user_author(self) -> bool:
        return self.is_author(current_user)

    @hybrid_property
    def is_public(self) -> bool:
        return self.is_shared if hasattr(self, "is_shared") else False

    # PERMISSIONS
    def can_view(self, user) -> bool:
        return (
            self == user  # for User
            or self.is_public
            or self.is_author(user)
            or self.can_edit(user)
            or (user.is_authenticated and user.has_permission("see-other"))
        )

    @property
    def can_current_user_view(self) -> bool:
        return self.can_view(user=current_user)

    def can_edit(self, user) -> bool:
        return (
            self == user
            or self.is_author(user)
            or (user.is_authenticated and user.has_permission("edit-other"))
        )

    @property
    def can_current_user_edit(self) -> bool:
        return self.can_edit(user=current_user)
