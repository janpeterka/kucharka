from app.models import User


def register(application):  # noqa: C901
    # DEV
    @application.cli.group()
    def dev():
        pass

    @dev.command()
    def reset_passwords():
        if application.config["APP_STATE"] == "production":
            print("ERROR: You cannot do this!")
            return

        user_count = len(User.load_all())
        print(f"INFO: will change password for {user_count} users..")

        for i, user in enumerate(User.load_all(ordered_by_name=False)[:10]):
            user.set_password(application.config["DEV_PASSWORD"])
            user.updated_by = 1
            user.edit()
            if i % int(user_count / 10) == 0:
                print(f"PROGRESS: changed password for {i} users..")

        print("INFO: Password set")
