from flask import redirect, url_for
from flask_security import login_required, roles_accepted

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.tips import Tip


class AdminStatisticsView(HelperFlaskView):
    decorators = [login_required, roles_accepted("admin", "application_manager")]

    def index(self):
        return self.template(template_name="admin/index.html.j2")

    def conversion_index(self):
        return redirect(url_for("ConversionsView:index"))

    def measurements_index(self):
        return redirect(url_for("MeasurementsView:index"))

    def recipe_categories_index(self):
        return redirect(url_for("RecipeCategoriesView:index"))

    def ingredient_categories_index(self):
        return redirect(url_for("IngredientCategoriesView:index"))

    def public_ingredients_index(self):
        return redirect(url_for("PublicIngredientsView:index"))

    def tips_index(self):
        return redirect(url_for("TipsView:index"))

    def unapproved_tips_count(self):
        self.unapproved_tips = Tip.unapproved_tips()
        self.notification_count = len(self.unapproved_tips)
        return self.template(template_name="admin/_admin_notification_count.html.j2")

    def admin_notification_count(self):
        self.unapproved_tips = Tip.unapproved_tips()
        self.notification_count = len(self.unapproved_tips)
        return self.template(template_name="admin/_admin_notification_count.html.j2")
