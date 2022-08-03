from flask import redirect, url_for, request
from flask_security import login_required, current_user

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.form import create_form

from app.models import PortionType
from app.forms import PortionTypeForm


class PortionTypeView(HelperFlaskView):
    decorators = [login_required]

    def index(self):
        return self.template()

    def new(self):
        self.form = create_form(PortionTypeForm)

        return self.template()

    def post(self):
        form = PortionTypeForm(request.form)

        if not form.validate_on_submit():
            return self.template("new"), 422

        portion_type = PortionType(author=current_user)
        portion_type.fill(form)
        portion_type.save()

        return redirect(request.referrer)
        # return redirect(url_for("PortionTypeView:index"))
