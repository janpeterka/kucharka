from flask import request, url_for, redirect, flash

from flask_security import login_required, current_user

from app.helpers.form import create_form, save_form_to_session
from app.helpers.helper_flask_view import HelperFlaskView

from app.models.users import User

from app.controllers.forms.users import UsersForm


class UsersView(HelperFlaskView):
    decorators = [login_required]

    @login_required
    def before_request(self, name, id=None, *args, **kwargs):
        if "id" in request.args:
            id = request.args.get("id")

        self.user = User.load(id)
        if not self.user:
            self.user = current_user

        self.validate_operation(id, self.user)

    def before_edit(self):
        self.user_form = create_form(UsersForm, obj=self.user)

    def index(self):
        if not current_user.has_permission("manage-users"):
            return redirect(url_for("UsersView:show"))

        self.users = User.load_all()
        return self.template()

    def show(self, **kwargs):
        return self.template()

    def edit(self):
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

    # @permissions_required("login-as")
    # def login_as(self, user_id, back=False):
    #     if "back" in request.args:
    #         back = request.args["back"]
    #     session.pop("logged_from_admin", None)
    #     if not back:
    #         session["logged_from_admin"] = current_user.id
    #     login_user(User.load(user_id))
    #     return redirect(url_for("IndexView:index"))
