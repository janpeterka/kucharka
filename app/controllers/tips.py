from flask import redirect, url_for, request
from flask_security import login_required, permissions_required
from flask_classful import route

from app import turbo

from app.models.tips import Tip

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.turbo_flash import turbo_flash as flash


class TipsView(HelperFlaskView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, id=None, *args, **kwargs):
        self.tip = Tip.load(id)
        self.validate_operation(id, self.tip)

    def before_manage(self):
        self.tips = Tip.load_all()
        self.unapproved_tips = Tip.unapproved_tips()
        self.unapproved_tips.sort(key=lambda x: x.created_at, reverse=True)
        self.approved_tips = Tip.approved_tips()
        self.approved_tips.sort(key=lambda x: x.created_at, reverse=True)
        self.disapproved_tips = Tip.disapproved_tips()
        self.disapproved_tips.sort(key=lambda x: x.created_at, reverse=True)

    @permissions_required("manage-application")
    def manage(self):
        return self.template()

    @route("tips")
    def index(self):
        self.tips = Tip.approved_tips()
        return self.template()

    @route("add-tip", methods=["POST"])
    def add_tip(self):
        tip = Tip()
        tip.description = request.form["description"]

        if tip.save():
            flash("Tip byl přidán ke schválení, děkujeme!", "success")
        else:
            flash("Něco se nepovedlo.", "error")

        return redirect(url_for("TipsView:index"))

    @permissions_required("manage-application")
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

    @permissions_required("manage-application")
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
