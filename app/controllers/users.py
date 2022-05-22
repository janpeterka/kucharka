from flask import request, url_for, redirect, flash
from flask_classful import route
from flask_security import login_required, current_user

from app.helpers.form import create_form, save_form_to_session
from app.helpers.helper_flask_view import HelperFlaskView

from app.models import User
from app.forms import UserForm, SetPasswordForm


class UserView(HelperFlaskView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, id=None, *args, **kwargs):
        if "id" in request.args:
            id = request.args.get("id")

        self.user = User.load(id)
        if not self.user:
            self.user = current_user

    def before_show(self, **kwargs):
        self.validate_show(self.user)

    def before_edit(self):
        self.validate_edit(self.user)

    def index(self):
        if not current_user.has_permission("manage-users"):
            return redirect(url_for("UserView:show"))

        self.users = User.load_all()

        return self.template()

    def show(self, **kwargs):
        return self.template()

    def edit(self):
        self.user_form = create_form(UserForm, obj=self.user)

        return self.template()

    def post(self):
        form = UserForm(request.form)
        del form.username

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("UserView:edit"))

        self.user.full_name = form.full_name.data

        if self.user.edit() is not None:
            flash("Uživatel byl upraven", "success")
        else:
            flash("Nepovedlo se změnit uživatele", "error")

        return redirect(url_for("UserView:show"))

    def set_password(self):
        self.form = SetPasswordForm()
        return self.template("_set_password")

    @route("set-password", methods=["POST"])
    def set_new_password(self):
        form = SetPasswordForm(request.form)
        self.user.set_password(form.password.data)
        self.user.save()
        flash("Heslo nastaveno")
        return redirect(url_for("UserView:show"))

    # @permissions_required("login-as")
    # def login_as(self, user_id, back=False):
    #     if "back" in request.args:
    #         back = request.args["back"]
    #     session.pop("logged_from_admin", None)
    #     if not back:
    #         session["logged_from_admin"] = current_user.id
    #     login_user(User.load(user_id))
    #     return redirect(url_for("IndexView:index"))
