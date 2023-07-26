from flask import render_template
from markupsafe import Markup
import os
from .utils import camelcase_to_snakecase
from .css import CSSClasses


class ComponentHelperMeta(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

        @classmethod
        def helper_method(cls, *args, **kwargs):
            return cls(*args, **kwargs).render()

        setattr(cls, "helper", helper_method)

        @classmethod
        def register_helper_method(cls, application, name: str = None):
            """creates `register_helper` method on class, which registers helper method on application

            [description]
            :param application: [description]
            :type application: Flask
            :param name: name of helper, called from jinja template, defaults to None
            :type name: str, optional
            """
            if name is None:
                name = camelcase_to_snakecase(cls.__name__)

            application.add_template_global(cls.helper, name=name)

        setattr(cls, "register_helper", register_helper_method)


class BaseComponent(metaclass=ComponentHelperMeta):
    """Base class for all TemplateComponents.

    provides `render` method, which renders template with attributes passed to it.

    :param DEFAULT_CLASSES: list of css classes to be added to the component
    :type DEFAULT_CLASSES: list
    :param folder: folder to look for template in, defaults to file name in snake_case
    :type folder: str (optional)
    :param file: template file name to render, defaults to component class name in snake_case
    :type file: str (optional)
    """

    DEFAULT_CLASSES = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs

        class_list = self.kwargs.pop("class", "").split(" ") + self.DEFAULT_CLASSES
        self.css_classes = CSSClasses(class_list)

    def render(self, remove_newlines: bool = True) -> Markup:
        html = render_template(self._template, **self._attributes)
        html = BaseComponent.clean_markup(html)

        return Markup(html)

    @staticmethod
    def clean_markup(html: str, remove_newlines: bool = True) -> str:
        if remove_newlines:
            html = html.replace("\n", "")
        while "  " in html:
            html = html.replace("  ", " ")
        html = html.replace(" >", ">")
        html = html.replace("> <", "><")
        html = html.replace('=" ', '="')
        html = html.replace(' "', '"')
        html = html.strip()

        return html

    @property
    def default_folder_name(self) -> str:
        if getattr(self, "folder", None) is not None:
            return self.folder
        else:
            return self._get_filename()

    @property
    def default_file_name(self) -> str:
        if getattr(self, "file", None) is not None:
            return self.file
        else:
            return camelcase_to_snakecase(self.__class__.__name__)

    @property
    def _template(self) -> str:
        folder = self.default_folder_name
        file = self.default_file_name
        filename = f"{file}.html.j2"

        return os.path.join("template_components", folder, filename)

    @property
    def _attributes(self) -> dict:
        # All public variables of the view are passed to template
        class_attributes = self.__class__.__dict__
        view_attributes = self.__dict__
        all_attributes = class_attributes | view_attributes
        public_attributes = {
            k: all_attributes[k] for k in all_attributes if not k.startswith("_")
        }

        # kwargs has higher priority, therefore rewrites public attributes
        merged_values = {**public_attributes, **self.kwargs}
        return merged_values

    def _get_filename(self):
        import inspect

        # Get the current class
        cls = type(self)

        # Retrieve the filename where the class is defined
        filename = inspect.getfile(cls)

        # Get only the filename without directories and extensions
        filename = os.path.splitext(os.path.basename(filename))[0]

        return filename


def register_helpers(
    application,
    package_name="kucharka.packages.template_components.components",
):
    import importlib
    import inspect

    # Import the package dynamically
    package = importlib.import_module(package_name)

    # Get all classes defined in the package
    classes = inspect.getmembers(package, inspect.isclass)

    for klassname, klass in classes:
        klass.register_helper(application)
        application.add_template_global(
            klass.helper, name=camelcase_to_snakecase(klassname)
        )
