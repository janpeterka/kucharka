from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired

from flask_wtf import FlaskForm


class AttendeeForm(FlaskForm):
    name = StringField("jméno", [InputRequired("jméno musí být vyplněno")])

    portion_size_ratio = SelectField(
        "velikost porce", choices=[(1, "normální"), (0.8, "malá")]
    )

    submit = SubmitField("přidat")
    update = SubmitField("upravit")
