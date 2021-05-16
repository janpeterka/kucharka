from flask_security import login_required, current_user

from app.helpers.helper_flask_view import HelperFlaskView


class DashboardView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "dashboard"

    def before_index(self):
        self.ingredients = current_user.ingredients

    def index(self):
        return self.template()
