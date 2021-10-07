from flask import request, redirect, url_for

from flask_classful import route

from app.helpers.helper_flask_view import HelperFlaskView
from app.helpers.form import create_form, save_form_to_session
from app.handlers.data import DataHandler


from app.models import *  # noqa: F401, F403, F406
from app.controllers.forms import *  # noqa: F401, F403, F406


class ExtendedFlaskView(HelperFlaskView):
    def before_request(self, name, id=None, *args, **kwargs):
        DataHandler.set_additional_request_data(item_type=self._attribute_name)

        # e.g. self.user = User.load(id)
        if id is not None and self._model_klass is not None:
            DataHandler.set_additional_request_data(item_id=id)

            self.object = (self._model_klass)().load(id)
            # e.g. self.user = user or self.user = None
            setattr(self, self._attribute_name, self.object)
        else:
            setattr(self, self._attribute_name, None)

    def before_new(self, *args, **kwargs):
        # e.g. self.form = create_form(UsersForm)
        if self._form_klass:
            self.form = create_form(self._form_klass)

    def before_edit(self, id, *args, **kwargs):
        # e.g. self.form = create_form(UserForm, obj=self.user)
        if self._form_klass:
            self.form = create_form(
                self._form_klass, obj=getattr(self, self._attribute_name)
            )

    def index(self, *args, **kwargs):
        return self.template()

    def new(self, *args, **kwargs):
        return self.template()

    def show(self, id, *args, **kwargs):
        return self.template()

    def edit(self, id, *args, **kwargs):
        return self.template()

    @route("post", methods=["POST"])
    def post(self):
        from flask_security import current_user

        form = self._form_klass(request.form)
        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for(f"{self._model_name}sView:new"))

        self.object = self._model_klass()
        self.object.author = current_user
        form.populate_obj(self.object)
        self.object.save()

        return redirect(url_for(f"{self._model_name}sView:show", id=self.object.id))

    @route("edit/<id>", methods=["POST"])
    def post_edit(self, id):
        form = self._form_klass(request.form)
        if not form.validate_on_submit():
            save_form_to_session(request.form)
            return redirect(url_for(f"{self._model_name}sView:edit", id=self.object.id))

        form.populate_obj(self.object)
        self.object.edit()

        return redirect(url_for(f"{self._model_name}sView:show", id=self.object.id))
