from flask_security import login_required

from app.helpers.helper_flask_view import HelperFlaskView

from app.models.tips import Tip


class AdminStatisticsView(HelperFlaskView):
    decorators = [login_required]

    def unapproved_tips_count(self):
        self.unapproved_tips = Tip.unapproved_tips()
        self.notification_count = len(self.unapproved_tips)
        return self.template(template_name="admin/_admin_notification_count.html.j2")

    def admin_notification_count(self):
        self.unapproved_tips = Tip.unapproved_tips()
        self.notification_count = len(self.unapproved_tips)
        return self.template(template_name="admin/_admin_notification_count.html.j2")
