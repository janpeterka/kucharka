from flask import request, url_for, redirect, flash

from flask_security import login_required, current_user

from app.helpers.form import create_form, save_form_to_session
from app.helpers.helper_flask_view import HelperFlaskView

from app.models.users import User

from app.controllers.forms.users import UsersForm


class UsersView(HelperFlaskView):
    decorators = [login_required]

    def before_request(self, name, id=None, *args, **kwargs):
        self.user = User.load(id)
        self.user = current_user if self.user is None else self.user

        self.validate_operation(id, self.user)

    def index(self):
        return redirect(url_for("UsersView:show"))

    def show(self, **kwargs):
        return self.template()

    def edit(self):
        self.user_form = create_form(UsersForm, obj=self.user)
        # self.password_form = create_form(ChangePasswordForm)

        return self.template()

    def post(self, page_type=None):
        form = UsersForm(request.form)
        del form.username

        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for("UsersView:edit"))

        self.user.full_name = form.full_name.data

        if self.user.edit() is not None:
            flash("Uživatel byl upraven", "success")
        else:
            flash("Nepovedlo se změnit uživatele", "error")

        return redirect(url_for("UsersView:show"))

    # @admin_required
    # def show_all(self):
    #     users = User.load_all()
    #     return self.template("admin/users/all.html.j2", users=users)

    # @admin_required
    # def login_as(self, user_id, back=False):
    #     if "back" in request.args:
    #         back = request.args["back"]
    #     session.pop("logged_from_admin", None)
    #     if not back:
    #         session["logged_from_admin"] = current_user.id
    #     login_user(User.load(user_id))
    #     return redirect(url_for("IndexView:index"))
