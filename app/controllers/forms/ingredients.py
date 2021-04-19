from wtforms import StringField, SubmitField, SelectField
from wtforms import validators

from flask_wtf import FlaskForm

from app.controllers.forms.custom import ComaFloatField

from wtforms.widgets import TextArea


class IngredientsForm(FlaskForm):
    # Required

    name = StringField(
        "Název suroviny", [validators.InputRequired("Název musí být vyplněn")]
    )

    description = StringField("Popis", widget=TextArea())

    measurement = SelectField(
        "Měřím v",
        choices=[("gram", "gramech"), ("kus", "kusech"), ("mililitr", "mililitrech")],
    )

    protein = ComaFloatField(
        "Množství bílkovin / 100 g",
        [
            validators.Optional(),
            validators.NumberRange(0, 100, "Musí být mezi 0 a 100"),
        ],
    )
    sugar = ComaFloatField(
        "Množství sacharidů / 100 g",
        [
            validators.Optional(),
            validators.NumberRange(0, 100, "Musí být mezi 0 a 100"),
        ],
    )
    fat = ComaFloatField(
        "Množství tuku / 100 g",
        [
            validators.Optional(),
            validators.NumberRange(0, 100, "Musí být mezi 0 a 100"),
        ],
    )
    calorie = ComaFloatField("Energie (kJ) / 100 g", [validators.Optional()])
    submit = SubmitField("Přidat surovinu")
