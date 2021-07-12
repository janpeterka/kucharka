from flask import redirect, url_for
from flask_security import login_required, roles_accepted

from app import turbo

from flask_classful import route

from app.models.tips import Tip

from app.helpers.helper_flask_view import HelperFlaskView


class TipsView(HelperFlaskView):
    decorators = [login_required, roles_accepted("admin", "application_manager")]

    @login_required
    def before_request(self, name, id=None, *args, **kwargs):
        self.tip = Tip.load(id)
        self.validate_operation(id, self.tip)

    def before_index(self):
        self.tips = Tip.load_all()
        self.unapproved_tips = Tip.unapproved_tips()
        self.unapproved_tips.sort(key=lambda x: x.created_at, reverse=True)
        self.approved_tips = Tip.approved_tips()
        self.approved_tips.sort(key=lambda x: x.created_at, reverse=True)
        self.disapproved_tips = Tip.disapproved_tips()
        self.disapproved_tips.sort(key=lambda x: x.created_at, reverse=True)

    def index(self):
        return self.template()

    @route("/approve/<id>", methods=["POST"])
    def approve(self, id):
        self.tip.approve()

        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.remove(target=f"tip-{id}"),
                    turbo.prepend(
                        self.template(template_name="_tip"), target="approved-tips"
                    ),
                ]
            )
        else:
            return redirect(url_for("TipsView:index"))

    @route("/disapprove/<id>", methods=["POST"])
    def disapprove(self, id):
        self.tip.disapprove()

        if turbo.can_stream():
            return turbo.stream(
                [
                    turbo.remove(target=f"tip-{id}"),
                    turbo.prepend(
                        self.template(template_name="_tip"), target="disapproved-tips"
                    ),
                ]
            )
        else:
            return redirect(url_for("TipsView:index"))
