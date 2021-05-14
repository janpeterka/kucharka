from flask_security import login_required, current_user

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.ingredients import Ingredient


class DashboardView(HelperFlaskView):
    decorators = [login_required]
    template_folder = "dashboard"

    @login_required
    def before_index(self):
        self.ingredients = [
            i for i in current_user.ingredients if i not in Ingredient.load_all_public()
        ]

    def index(self):
        return self.template()
