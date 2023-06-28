from flask import current_app as application

from flask_security import current_user

from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.hybrid import hybrid_property

from app import db


# Custom methods for all my classes
class BaseMixin(object):
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
    def load_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def load_all(cls, ordered_by_name=True, **kwargs):
        from unidecode import unidecode

        objects = cls.query.filter_by(**kwargs).all()

        if ordered_by_name and hasattr(cls, "name"):
            objects.sort(key=lambda x: unidecode(x.name.lower()))

        return objects

    @classmethod
    def load_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def load_all_by_attribute(cls, attribute, value):
        if not hasattr(cls, attribute):
            raise AttributeError

        return cls.query.filter_by(**{attribute: value}).all()

    # OTHER LOADING
    # @classmethod
    # def created_at_date(cls, date):
    #     if hasattr(cls, "created_at"):
    #         attr = "created_at"
    #     else:
    #         raise AttributeError('No "created_at" for created_at_date')

    #     return cls.query.filter(func.DATE(getattr(cls, attr)) == date).all()

    # @classmethod
    # def created_recently(cls, days=30):
    #     date_from = datetime.date.today() - datetime.timedelta(days=days)
    #     if hasattr(cls, "created_at"):
    #         attr = "created_at"
    #     else:
    #         raise AttributeError('No "created_at" for created_recently')

    #     return cls.query.filter(getattr(cls, attr) > date_from).all()

    # @classmethod
    # def created_in_last_30_days(cls):
    #     return cls.created_recently(days=30)

    # DATABASE OPERATIONS

    def edit(self, **kw):
        try:
            if hasattr(self, "updated_by"):
                if current_user and current_user.is_authenticated:
                    self.updated_by = current_user.id
                # else is when we edit from the shell/scripts

            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            application.logger.error(f"Edit error: {e}")
            return False

    def save(self, **kw):
        """Saves (new) object"""
        try:
            db.session.add(self)
            db.session.commit()
            return True

        except DatabaseError as e:
            db.session.rollback()
            application.logger.error(f"Save error: {e}")
            return False

    def remove(self, **kw):
        """Deletes object"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except DatabaseError as e:
            db.session.rollback()
            application.logger.error(f"Remove error: {e}")
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
            application.logger.error(f"Expire error: {e}")
            return False

    def refresh(self, **kw):
        try:
            db.session.refresh(self)
            return True
        except Exception as e:
            db.session.rollback()
            application.logger.error(f"Refresh error: {e}")
            return False

    def reload(self):
        return type(self).load(self.id)

    # PROPERTIES

    def is_author(self, user) -> bool:
        if not hasattr(self, "author"):
            return False

        return self.author == user  # type: ignore

    @property
    def is_current_user_author(self) -> bool:
        return self.is_author(current_user)

    @hybrid_property
    def is_public(self) -> bool:
        if not hasattr(self, "is_shared"):
            return False

        return self.is_shared  # type: ignore

    # PERMISSIONS
    def can_view(self, user) -> bool:
        return (
            self == user  # for User
            or self.is_public
            or self.is_author(user)
            or self.can_edit(user)
            or (user.is_authenticated and user.has_permission("see-other"))
        )

    def can_edit(self, user) -> bool:
        return (
            self == user
            or self.is_author(user)
            or (user.is_authenticated and user.has_permission("edit-other"))
        )

    def can_delete(self, user) -> bool:
        return self.can_edit(user)

    @property
    def can_current_user_view(self) -> bool:
        return self.can_view(user=current_user)

    @property
    def can_current_user_edit(self) -> bool:
        return self.can_edit(user=current_user)

    @property
    def can_current_user_delete(self) -> bool:
        return self.can_delete(user=current_user)
