from flask import redirect, url_for
from flask_security import login_required, permissions_required
from flask_classful import route

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.tips import Tip


class AdminView(HelperFlaskView):
    decorators = [login_required, permissions_required("manage-application")]

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

    @route("toggle_admin", methods=["POST"])
    def toggle_admin(self):
        from flask import session, request

        if session.get("as_commoner", False):
            session["as_commoner"] = False
        else:
            session["as_commoner"] = True

        return redirect(request.referrer)
