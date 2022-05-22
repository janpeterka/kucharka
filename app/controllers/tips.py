from flask import redirect, url_for, request, flash
from flask_security import login_required, permissions_required
from flask_classful import route

from app.models.tips import Tip

from app.helpers.helper_flask_view import HelperFlaskView


class TipView(HelperFlaskView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, id=None, *args, **kwargs):
        self.tip = Tip.load(id)

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

    def index(self):
        self.tips = Tip.approved_tips()

        return self.template()

    @route("add-tip", methods=["POST"])
    def add_tip(self):
        tip = Tip()
        tip.description = request.form["description"]

        if tip.save():
            flash("tip byl přidán ke schválení, děkujeme!", "success")
        else:
            flash("něco se nepovedlo.", "error")

        return redirect(url_for("TipView:index"))

    @permissions_required("manage-application")
    @route("/approve/<id>", methods=["POST"])
    def approve(self, id):
        self.tip.approve()

        return redirect(url_for("TipView:manage"))

    @permissions_required("manage-application")
    @route("/disapprove/<id>", methods=["POST"])
    def disapprove(self, id):
        self.tip.disapprove()

        return redirect(url_for("TipView:manage"))
