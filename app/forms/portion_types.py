from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

from flask_wtf import FlaskForm

from .custom import CancelButtonField, UpdateButtonField, ComaFloatField


class PortionTypeForm(FlaskForm):
    name = StringField("jméno", [InputRequired("jméno musí být vyplněno")])
    size = ComaFloatField("velikost porce")

    submit = SubmitField("přidat")
    update = UpdateButtonField("upravit")
    cancel = CancelButtonField("zrušit")
