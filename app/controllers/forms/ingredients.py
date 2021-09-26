from wtforms import StringField, SubmitField, BooleanField
from wtforms import validators

from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField  # , QuerySelectMultipleField

from wtforms.widgets import TextArea

from app.controllers.forms.custom import ComaFloatField


def categories():
    from app.models.ingredient_categories import IngredientCategory

    return IngredientCategory.load_all()


def measurements():
    from app.models.measurements import Measurement

    return Measurement.load_all()


class IngredientsForm(FlaskForm):

    name = StringField(
        "Název suroviny", [validators.InputRequired("Název musí být vyplněn")]
    )

    description = StringField("Popis", widget=TextArea())

    measurement = QuerySelectField(
        "Počítané v", query_factory=measurements, get_label="name", allow_blank=True
    )
    category = QuerySelectField(
        "Kategorie", query_factory=categories, get_label="name", allow_blank=True
    )

    is_vegetarian = BooleanField("vegetariánské")
    is_vegan = BooleanField("veganské")
    lactose_free = BooleanField("bez laktózy")
    gluten_free = BooleanField("bez lepku")

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
