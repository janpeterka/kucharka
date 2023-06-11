from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, BooleanField

from wtforms.validators import InputRequired
from wtforms.widgets import NumberInput

from .custom import ComaFloatField


class RecipeIngredientForm(FlaskForm):
    amount = ComaFloatField("množství", [InputRequired()], widget=NumberInput(step=0.1))
    is_measured = BooleanField("měřené?", default=True)
    comment = StringField("komentář")

    submit = SubmitField("přidat surovinu do receptu")
