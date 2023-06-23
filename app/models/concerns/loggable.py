from sqlalchemy.orm import declared_attr
from sqlalchemy.sql import func
from sqlalchemy import event

from app import db


class Loggable:
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    @declared_attr
    def created_by(cls):
        return db.Column(db.ForeignKey("users.id"), nullable=False, index=True)

    @declared_attr
    def author(cls):
        return db.relationship(
            "User", primaryjoin=f"User.id == {cls.__name__}.created_by", uselist=False
        )

    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    @declared_attr
    def updated_by(cls):
        return db.Column(db.ForeignKey("users.id"))


@event.listens_for(Loggable, "init", propagate=True)
def intercept_init(instance, args, kwargs):
    from flask_security import current_user

    # check if created_by is already set
    if getattr(instance, "created_by", None):
        return

    if not (current_user and current_user.is_authenticated):
        return

    instance.created_by = current_user.id
