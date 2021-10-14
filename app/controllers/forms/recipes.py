from wtforms import StringField, SubmitField, IntegerField
from wtforms import validators
from wtforms.widgets import TextArea

from flask_wtf import FlaskForm

from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField


def ingredients():
    from app.models.ingredients import Ingredient

    return Ingredient.load_all_in_public_recipes()


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
    name = StringField(
        "Název receptu", [validators.InputRequired("Název musí být vyplněn")]
    )

    description = StringField("Popis", widget=TextArea())

    category = QuerySelectField("Kategorie", query_factory=categories, allow_blank=True)
    portion_count = IntegerField("Počet porcí", [validators.NumberRange(min=1)])

    labels = QuerySelectMultipleField("Dietní omezení", query_factory=dietary_labels)

    submit = SubmitField("Přidat recept")

    def set_category(self, categories):
        self.category.choices = [
            (category.id, category.name) for category in categories
        ]

    def set_all(self, **kwargs):
        if "categories" in kwargs:
            self.set_category(kwargs["categories"])


class RecipeFilterForm(FlaskForm):
    ingredient = QuerySelectField(
        "Surovina", query_factory=ingredients, allow_blank=True
    )
    category = QuerySelectField("Kategorie", query_factory=categories, allow_blank=True)

    with_labels = QuerySelectMultipleField(
        "Dietní omezení", query_factory=dietary_labels
    )

    submit = SubmitField("Filtrovat")
