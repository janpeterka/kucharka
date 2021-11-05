from flask_security import login_required, current_user

from app.helpers.helper_flask_view import HelperFlaskView


class DashboardView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "dashboard"

    def index(self):
        self.ingredients = current_user.personal_ingredients
        return self.template()

    def tasks(self):
        return self.template(template_name="_tasks")

    def current(self):
        # from time import sleep
        # sleep(10)
        return self.template(template_name="_current")
