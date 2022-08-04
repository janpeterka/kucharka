from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired

from flask_wtf import FlaskForm

from .custom import CancelButtonField, UpdateButtonField


class PortionTypeForm(FlaskForm):
    name = StringField("jméno", [InputRequired("jméno musí být vyplněno")])
    size = IntegerField("velikost porce (% z běžné)")

    submit = SubmitField("přidat typ porce")
    update = UpdateButtonField("upravit")
    cancel = CancelButtonField("zrušit")
