from wtforms import StringField, SubmitField
from wtforms import validators

from flask_wtf import FlaskForm


class UsersForm(FlaskForm):
    username = StringField(
        "Přihlašovací email", [validators.InputRequired("Email musí být vyplněn")]
    )
    full_name = StringField(
        "Jméno", [validators.InputRequired("Jméno musí být vyplněno")]
    )
    submit = SubmitField("Upravit")
