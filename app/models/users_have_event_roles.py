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
    event = db.relationship("Event", back_populates="user_roles")

    @staticmethod
    def load_by_event_and_user(event, user):
        return UserHasEventRole.query.filter_by(
            event_id=event.id, user_id=user.id
        ).first()
