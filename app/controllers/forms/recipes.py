from wtforms import StringField, SubmitField, SelectField
from wtforms import validators

from flask_wtf import FlaskForm

from wtforms.widgets import TextArea


class RecipesForm(FlaskForm):
    name = StringField(
        "Název suroviny", [validators.InputRequired("Název musí být vyplněn")]
    )

    description = StringField("Popis", widget=TextArea())

    category = SelectField("Kategorie", coerce=int)

    submit = SubmitField("Přidat recept")

    def set_category(self, categories):
        self.category.choices = [
            (category.id, category.name) for category in categories
        ]

    def set_all(self, **kwargs):
        if "categories" in kwargs:
            self.set_category(kwargs["categories"])
