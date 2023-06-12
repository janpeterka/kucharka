from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField

from wtforms.validators import InputRequired, NumberRange
from wtforms.widgets import NumberInput

from .custom import ComaFloatField


class RecipeIngredientForm(FlaskForm):
    amount = ComaFloatField(
        "množství", [InputRequired(), NumberRange(min=0)], widget=NumberInput(step=0.1)
    )
    comment = StringField("komentář")

    submit = SubmitField("přidat surovinu do receptu")
