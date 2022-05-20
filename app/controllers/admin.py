from flask import redirect, url_for
from flask_security import login_required, permissions_required

# from flask_classful import route

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.tips import Tip


class AdminView(HelperFlaskView):
    decorators = [login_required, permissions_required("manage-application")]

    def index(self):
        return self.template(template_name="admin/index.html.j2")

    def conversion_index(self):
        return redirect(url_for("ConversionView:index"))

    def measurements_index(self):
        return redirect(url_for("MeasurementView:index"))

    def recipe_categories_index(self):
        return redirect(url_for("RecipeCategorieView:index"))

    def ingredient_categories_index(self):
        return redirect(url_for("IngredientCategorieView:index"))

    def public_ingredients_index(self):
        return redirect(url_for("PublicIngredientView:index"))

    def tips_index(self):
        return redirect(url_for("TipView:manage"))

    def files(self):
        return redirect(url_for("FileView:index"))

    def unapproved_tips_count(self):
        self.notification_count = self._unapproved_tips_count()
        return self.template(template_name="admin/_admin_notification_count.html.j2")

    def admin_notification_count(self):
        self.notification_count = self._unapproved_tips_count()
        return self.template(template_name="admin/_admin_notification_count.html.j2")

    def _unapproved_tips_count(self) -> int:
        return len(Tip.unapproved_tips())

    # @route("toggle_admin", methods=["POST"])
    # def toggle_admin(self):
    #     from flask import session, request

    #     if session.get("as_commoner", False):
    #         session["as_commoner"] = False
    #     else:
    #         session["as_commoner"] = True

    #     return redirect(request.referrer)
