from wtforms import BooleanField
from wtforms.widgets import SubmitInput


class ButtonField(BooleanField):
    widget = SubmitInput()

    def __init__(self, *args, **kwargs):
        self.default_classes = self.DEFAULT_CLASSES
        super().__init__(*args, **kwargs)

    @property
    def default_class(self):
        return " ".join(self.default_classes)


class CancelButtonField(ButtonField):
    DEFAULT_CLASSES = ["btn", "bg-color-secondary-action", "color-white"]


class UpdateButtonField(ButtonField):
    DEFAULT_CLASSES = ["btn", "bg-color-primary-action", "color-white"]
