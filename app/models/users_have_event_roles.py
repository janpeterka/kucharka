from app import db, BaseModel

from app.helpers.base_mixin import BaseMixin


class UserHasEventRole(BaseModel, BaseMixin):

    __tablename__ = "users_have_event_roles"

    event_id = db.Column(
        db.ForeignKey("events.id"), primary_key=True, nullable=False, index=True
    )
    user_id = db.Column(
        db.ForeignKey("users.id"), primary_key=True, nullable=False, index=True
    )
    role = db.Column(db.Enum("collaborator", "viewer"))

    user = db.relationship("User", backref="user_event_roles")
    event = db.relationship("Event", backref="event_user_roles")
