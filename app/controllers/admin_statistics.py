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

    @route("convert_recipes_to_labels", methods=["POST"])
    def convert_recipes_to_labels(self):
        # TODO: delete after using
        from app.models.labels import Label
        from app.models.recipes import Recipe

        for recipe in Recipe.load_all():
            if recipe.is_vegetarian:
                recipe.labels.append(Label.load_by_name("vegetarian"))

            if recipe.is_vegan:
                recipe.labels.append(Label.load_by_name("vegan"))

            if recipe.lactose_free:
                recipe.labels.append(Label.load_by_name("lactose_free"))

            if recipe.gluten_free:
                recipe.labels.append(Label.load_by_name("gluten_free"))

            recipe.edit()

        return redirect("AdminStatisticsView:index")
