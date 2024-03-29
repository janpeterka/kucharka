from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Optional, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.widgets import TextArea

from .custom import ComaFloatField


def categories():
    from app.models import IngredientCategory

    return IngredientCategory.load_all()


def measurements():
    from app.models import Measurement

    return Measurement.load_all()


class IngredientForm(FlaskForm):
    name = StringField("název suroviny", [InputRequired("název musí být vyplněn")])

    description = StringField("popis", widget=TextArea())

    measurement = QuerySelectField(
        "počítané v", query_factory=measurements, allow_blank=True
    )
    category = QuerySelectField("kategorie", query_factory=categories, allow_blank=True)

    protein = ComaFloatField(
        "bílkoviny / 100 g",
        [Optional(), NumberRange(0, 100, "musí být mezi 0 a 100")],
    )
    sugar = ComaFloatField(
        "sacharidy / 100 g",
        [Optional(), NumberRange(0, 100, "musí být mezi 0 a 100")],
    )
    fat = ComaFloatField(
        "tuky / 100 g",
        [Optional(), NumberRange(0, 100, "musí být mezi 0 a 100")],
    )
    calorie = ComaFloatField("energie (kJ) / 100 g", [Optional()])
    submit = SubmitField("přidat surovinu")
