from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired

from flask_wtf import FlaskForm


class UsersForm(FlaskForm):
    username = StringField(
        "Přihlašovací email", [InputRequired("E-mail musí být vyplněn")]
    )
    full_name = StringField("Jméno", [InputRequired("Jméno musí být vyplněno")])
    submit = SubmitField("Upravit")


class SetPasswordForm(FlaskForm):
    password = PasswordField("Nové heslo", [InputRequired("Musí být vyplněno")])
    submit = SubmitField("Nastavit")
