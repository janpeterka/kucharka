from app import db
from flask_security import current_user
from sqlalchemy.orm import declared_attr


class Collaborative:
    # collaborators = db.relationship(
    #     "User",
    #     secondary="users_have_event_roles",
    #     primaryjoin="and_(Event.id == UserHasEventRole.event_id, UserHasEventRole.role =='collaborator')",
    #     viewonly=True,
    # )

    @declared_attr
    def shared_with(self):
        return db.relationship(
            "User",
            secondary="users_have_event_roles",
            primaryjoin="Event.id == UserHasEventRole.event_id",
            viewonly=True,
        )

    @declared_attr
    def user_roles(self):
        return db.relationship(
            "UserHasEventRole",
            cascade="all, delete",
        )

    def user_role(self, user):
        roles = [user_role for user_role in self.user_roles if user_role.user == user]
        if not roles:
            return None
        elif len(roles) == 1:
            return roles[0].role
        else:
            raise Warning("User has multiple roles on this event")

    @property
    def connected_users(self) -> list:
        users = self.shared_with
        users.append(self.author)

        return users

    @property
    def other_user_ids(self) -> list:
        user_ids = [user.id for user in self.shared_with]
        user_ids.append(self.author.id)
        user_ids.remove(current_user.id)

        if len(user_ids) == 1:
            user_ids = user_ids[0]

        return user_ids

    @property
    def current_user_role(self):
        return self.user_role(current_user)
