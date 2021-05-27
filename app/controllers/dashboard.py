from flask_security import login_required, current_user

from app.helpers.helper_flask_view import HelperFlaskView


class DashboardView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "dashboard"

    def index(self):
        self.ingredients = current_user.ingredients
        return self.template()
