from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, NumberRange
from wtforms.widgets import TextArea

from flask_wtf import FlaskForm

from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField


def categories():
    from app.models.recipe_categories import RecipeCategory

    return RecipeCategory.load_all()


def measurements():
    from app.models.measurements import Measurement

    return Measurement.load_all()


def labels():
    from app.models.labels import Label

    return Label.load_all()


def dietary_labels():
    from app.models.labels import Label

    return Label.load_dietary()


class RecipesForm(FlaskForm):
    name = StringField("Název receptu", [InputRequired("Název musí být vyplněn")])

    description = StringField("Popis", widget=TextArea())

    category = QuerySelectField("Kategorie", query_factory=categories, allow_blank=True)
    portion_count = IntegerField(
        "Počet porcí", [NumberRange(message="Musí být alespoň jedna porce", min=1)]
    )

    labels = QuerySelectMultipleField("Dietní omezení", query_factory=dietary_labels)

    submit = SubmitField("Přidat recept")
