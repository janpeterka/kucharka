from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired

from flask_wtf import FlaskForm


class UserForm(FlaskForm):
    username = StringField(
        "přihlašovací email", [InputRequired("e-mail musí být vyplněn")]
    )
    full_name = StringField("jméno", [InputRequired("jméno musí být vyplněno")])

    submit = SubmitField("upravit")


class SetPasswordForm(FlaskForm):
    password = PasswordField("nové heslo", [InputRequired("heslo musí být vyplněno")])

    submit = SubmitField("nastavit")
