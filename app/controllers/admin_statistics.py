from flask import redirect
from flask_classful import route
from flask_security import login_required, roles_accepted

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.tips import Tip


class AdminStatisticsView(HelperFlaskView):
    decorators = [login_required, roles_accepted("admin", "application_manager")]

    def index(self):
        return self.template(template_name="admin/index.html.j2")

    def unapproved_tips_count(self):
        self.unapproved_tips = Tip.unapproved_tips()
        self.notification_count = len(self.unapproved_tips)
        return self.template(template_name="admin/_admin_notification_count.html.j2")

    def admin_notification_count(self):
        self.unapproved_tips = Tip.unapproved_tips()
        self.notification_count = len(self.unapproved_tips)
        return self.template(template_name="admin/_admin_notification_count.html.j2")

    @route("convert_ingredients_to_labels", methods=["POST"])
    def convert_ingredients_to_labels(self):
        # TODO: delete after using
        from app.models.labels import Label
        from app.models.ingredients import Ingredient

        for ingredient in Ingredient.load_all():
            if ingredient.is_vegetarian:
                ingredient.labels.append(Label.load_by_name("vegetarian"))

            if ingredient.is_vegan:
                ingredient.labels.append(Label.load_by_name("vegan"))

            if ingredient.lactose_free:
                ingredient.labels.append(Label.load_by_name("lactose_free"))

            if ingredient.gluten_free:
                ingredient.labels.append(Label.load_by_name("gluten_free"))

            ingredient.edit()

        return redirect("AdminStatisticsView:index")
