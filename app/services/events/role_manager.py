from app.models import UserHasEventRole


class EventRoleManager:
    @staticmethod
    def add_user_role(event, user, role):
        event_role = UserHasEventRole(event=event, user=user, role=role)
        event_role.save()

    @staticmethod
    def change_user_role(event, user, role):
        event_role = UserHasEventRole.load_by_event_and_user(event=event, user=user)
        event_role.role = role
        event_role.save()

    @staticmethod
    def remove_user_role(event, user):
        event_role = UserHasEventRole.load_by_event_and_user(event=event, user=user)
        event_role.delete()
