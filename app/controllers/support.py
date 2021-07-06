from flask import redirect, request, url_for, flash
from flask import render_template as template

from flask_classful import FlaskView, route

# from flask_security import current_user, login_required

# from app.handlers.mail import MailSender

# from app.controllers.forms.support import FeedbackForm

from app.models.tips import Tip


class SupportView(FlaskView):
    @route("terms")
    def terms(self):
        return template("support/terms.html.j2")

    @route("privacy")
    def privacy(self):
        return template("support/privacy.html.j2")

    @route("facebook")
    def facebook_redirect(self):
        return redirect("https://www.facebook.com/skautskakucharka")

    @route("tips")
    def tips(self):
        tips = Tip.approved_tips()
        return template("support/tips.html.j2", tips=tips)

    @route("add-tip", methods=["POST"])
    def add_tip(self):
        tip = Tip()
        tip.description = request.form["description"]

        if tip.save():
            flash("Tip byl přidán ke schválení, děkujeme!", "success")
        else:
            flash("Něco se nepovedlo.", "error")

        return redirect(url_for("SupportView:tips"))

    # @route("/feedback", methods=["GET", "POST"])
    # @login_required
    # def feedback(self):
    #     from werkzeug.datastructures import CombinedMultiDict

    #     form = FeedbackForm(CombinedMultiDict((request.files, request.form)))
    #     if request.method == "GET":
    #         return template("support/feedback.html.j2", form=form)
    #     elif request.method == "POST":
    #         if not form.validate_on_submit():
    #             return template("support/feedback.html.j2", form=form)

    #         attachments = []
    #         if form.feedback_file.data:
    #             attachments = [form.feedback_file.data]

    #         MailSender().send_email(
    #             subject="[ketocalc] [{}]".format(form.option.data),
    #             sender="ketocalc",
    #             recipient_mails=["janmpeterka+skautskakucharkafeedback@gmail.com"],
    #             text_body="Message: {}\n Send by: {} [user: {}]".format(
    #                 form.message.data, form.email.data, current_user.username
    #             ),
    #             html_body=None,
    #             attachments=attachments,
    #         )

    #         flash("Vaše připomínka byla zaslána na vyšší místa.", "success")
    #         return redirect(url_for("DashboardView:index"))

    # @route("download/<filename>/", methods=["GET"])
    # def download(self, filename):
    #     PATH = os.path.dirname(os.path.realpath(__file__))
    #     FILES_PATH = os.path.join(PATH, "../public/files/")
    #     return send_file(
    #         os.path.join(FILES_PATH, filename), attachment_filename=filename,
    #     )
