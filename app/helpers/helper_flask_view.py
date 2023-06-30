import inspect
import re

from flask import abort
from flask import render_template as template

from flask_classful import FlaskView

from app.models import *  # noqa: F401, F403, F406
from app.forms import *  # noqa: F401, F403, F406


class HelperFlaskView(FlaskView):
    def validate_create(self, klass):
        self._validate_operation(klass)

        if not klass.can_current_user_create():
            abort(403)

    def validate_show(self, instance):
        self._validate_operation(instance)

        if not instance.can_current_user_view:
            abort(403)

    def validate_edit(self, instance):
        self._validate_operation(instance)

        if not instance.can_current_user_edit:
            abort(403)

    def validate_delete(self, instance):
        self._validate_operation(instance)

        if not instance.can_current_user_delete:
            abort(403)

    def _validate_operation(self, instance_or_klass):
        # if object_id is not None and instance is None:
        if instance_or_klass is None:
            abort(404)

    def template(self, template_name=None, *args, **kwargs):
        # Template name is given from view and method names if not provided
        calling_method = inspect.stack()[1].function

        if template_name is None:
            template_name = f"{self._template_folder}/{calling_method}.html.j2"
            # TODO: what if i want to force location?
        elif "/" in template_name or ".html.j2" in template_name:
            template_name = template_name
        else:
            template_name = f"{self._template_folder}/{template_name}.html.j2"

        # All public variables of the view are passed to template
        view_attributes = self.__dict__
        public_attributes = {
            k: view_attributes[k] for k in view_attributes if not k.startswith("_")
        }

        # kwargs has higher priority, therefore rewrites public attributes
        merged_values = public_attributes | kwargs

        return template(template_name, **merged_values)

    @property
    def _model_name(self):
        # e.g. User
        if type(self).__name__.endswith("View"):
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
        # e.g. class <UserForm>
        try:
            form_klass = globals()[self._form_name]
        except KeyError:
            form_klass = None

        return form_klass

    @property
    def _attribute_name(self):
        if hasattr(self, "attribute_name"):
            return self.attribute_name
        # e.g. measurement
        model_name = self._model_name
        return re.sub("(?!^)([A-Z]+)", r"_\1", model_name).lower()

    @property
    def _plural_attribute_name(self):
        if hasattr(self, "plural_attribute_name"):
            return self.plural_attribute_name
        else:
            return f"{self._attribute_name}s"

    @property
    def _form_name(self):
        return f"{self._model_name}sForm"

    @property
    def _template_folder(self):
        if hasattr(self, "template_folder"):
            return self.template_folder
        else:
            return f"{self._attribute_name}s"

    @property
    def _instance(self):
        return (
            getattr(self, self.instance_name)
            if hasattr(self, "instance_name")
            else getattr(self, self._attribute_name)
        )
