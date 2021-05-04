from wtforms import StringField, SubmitField, SelectField, BooleanField
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

    measurement = SelectField("Počítané v", coerce=int)
    category = SelectField("Kategorie", coerce=int)

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

    def set_measurement(self, measurements):
        self.measurement.choices = [
            (measurement.id, measurement.name) for measurement in measurements
        ]

    def set_category(self, categories):
        self.category.choices = [
            (category.id, category.name) for category in categories
        ]

    def set_all(self, **kwargs):
        if "measurements" in kwargs:
            self.set_measurement(kwargs["measurements"])

        if "categories" in kwargs:
            self.set_category(kwargs["categories"])
