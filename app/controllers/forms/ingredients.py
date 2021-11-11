from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Optional, NumberRange

from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField

from wtforms.widgets import TextArea

from app.controllers.forms.custom import ComaFloatField


def categories():
    from app.models.ingredient_categories import IngredientCategory

    return IngredientCategory.load_all()


def measurements():
    from app.models.measurements import Measurement

    return Measurement.load_all()


class IngredientsForm(FlaskForm):

    name = StringField("Název suroviny", [InputRequired("Název musí být vyplněn")])

    description = StringField("Popis", widget=TextArea())

    measurement = QuerySelectField(
        "Počítané v", query_factory=measurements, allow_blank=True
    )
    category = QuerySelectField("Kategorie", query_factory=categories, allow_blank=True)

    protein = ComaFloatField(
        "Bílkoviny / 100 g",
        [Optional(), NumberRange(0, 100, "Musí být mezi 0 a 100")],
    )
    sugar = ComaFloatField(
        "Sacharidy / 100 g",
        [Optional(), NumberRange(0, 100, "Musí být mezi 0 a 100")],
    )
    fat = ComaFloatField(
        "Tuky / 100 g",
        [Optional(), NumberRange(0, 100, "Musí být mezi 0 a 100")],
    )
    calorie = ComaFloatField("Energie (kJ) / 100 g", [Optional()])
    submit = SubmitField("Přidat surovinu")
