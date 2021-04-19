import inspect
import re

from flask import render_template as template
from flask import request

from flask_classful import FlaskView

from app.helpers.form import create_form
from app.handlers.data import DataHandler

from app.models import *  # noqa: F401, F403, F406
from app.controllers.forms import *  # noqa: F401, F403, F406


class ExtendedFlaskView(FlaskView):
    """docstring for ExtendedFlaskView"""

    def before_request(self, name, id=None, *args, **kwargs):

        DataHandler.set_additional_request_data(item_type=self._attribute_name)

        # e.g. self.user = User.load(id)
        if id is not None and self._model_klass is not None:
            DataHandler.set_additional_request_data(item_type=id)

            instance = (self._model_klass)().load(id)
            # e.g. self.user = user or self.user = None
            setattr(self, self._attribute_name, instance)
        else:
            setattr(self, self._attribute_name, None)

    def before_new(self, *args, **kwargs):
        # e.g. self.form = create_form(UsersForm)
        self.form = create_form(self._form_klass)

    def before_edit(self, id, *args, **kwargs):
        # e.g. self.form = create_form(UserForm, obj=self.user)
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

    def not_logged_in(self, *args, **kwargs):
        message = request.args.get(
            "message", "Tato funkce je přístupná pouze pro přihlášené uživatele."
        )
        return template("not_logged_in.html.j2", message=message)

    def template(self, template_name=None, **kwargs):
        # Template name is given from view and method names if not provided
        calling_method = inspect.stack()[1].function

        if hasattr(self, "template_folder"):
            template_folder = self.template_folder
        else:
            template_folder = f"{self._attribute_name}s"

        if template_name is None:
            template_name = f"{template_folder}/{calling_method}.html.j2"

        # All public variables of the view are passed to template
        view_attributes = self.__dict__
        public_attributes = {
            k: view_attributes[k] for k in view_attributes if not k.startswith("_")
        }

        # kwargs has higher priority, therefore rewrites public attributes
        merged_values = {**public_attributes, **kwargs}

        return template(template_name, **merged_values)

    @property
    def _model_name(self):
        # e.g. User
        if type(self).__name__.endswith("sView"):
            model_name = type(self).__name__.replace("sView", "")
        elif type(self).__name__.endswith("View"):
            model_name = type(self).__name__.replace("View", "")
        else:
            raise AttributeError("Controller name not ending with 'View'")

        return model_name

    @property
    def _model_klass(self):
        # e.g. class <User>
        try:
            model_klass = globals()[self._model_name]
        except KeyError:
            model_klass = None
        return model_klass

    @property
    def _form_klass(self):
        # e.g. class <UsersForm>
        try:
            form_klass = globals()[self._form_name]
        except KeyError:
            form_klass = None

        return form_klass

    @property
    def _attribute_name(self):
        # e.g. user
        model_name = self._model_name
        snake_model_name = re.sub("(?!^)([A-Z]+)", r"_\1", model_name).lower()
        return snake_model_name

    @property
    def _form_name(self):
        # e.g. UsersForm
        form_name = f"{self._model_name}sForm"
        return form_name

    @property
    def _template_folder(self):
        if hasattr(self, "template_folder"):
            return self.template_folder
        else:
            self.template_folder = self._attribute_name + "s"

    # def new(self):
    #     self.form = create_form(self.form_klass)
    #     return self.template()

    # def post(self):
    #     form = self.form_klass(request.form)
    #     if not form.validate_on_submit():
    #         save_form_to_session(request.form)
    #         return redirect(url_for("{}sView:new".format(self.model_name)))

    #     class_object = self.model_klass()
    #     form.populate_obj(class_object)
    #     if not class_object.save():
    #         # if save fails
    #         abort(500)

    #     return redirect(
    #         url_for("{}sView:show".format(self.model_name), id=class_object.id)
    #     )

    # @route("<id>/edit", methods=["POST"])
    # def post_edit(self, id):
    #     form = self.form_klass(request.form)
    #     if not form.validate_on_submit():
    #         save_form_to_session(request.form)
    #         return redirect(url_for("{}sView:edit".format(self.model_name)))

    #     form.populate_obj(self.object)
    #     self.object.edit()

    #     return redirect(
    #         url_for("{}sView:show".format(self.model_name), id=self.object.id,)
    #     )

    # def edit(self, id):
    #     form = create_form(self.form_klass, obj=self.object)
    #     return template(
    #         "{}s/edit.html.j2".format(self.attribute_name),
    #         form=form,
    #         id=self.object.id,
    #     )
