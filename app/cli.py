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

        for user in User.load_all():
            user.set_password(application.config["DEV_PASSWORD"])
            user.updated_by = 1
            user.edit()

        print("INFO: Password set")

    # ONE-OFFS

    @application.cli.group()
    def one_offs():
        pass

    @one_offs.command()
    def add_base_portion_type():
        from app.tasks.one_offs.add_base_portion_type import add_base_portion_type

        add_base_portion_type()
