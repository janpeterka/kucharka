from wtforms import StringField, SubmitField, SelectField, IntegerField, BooleanField
from wtforms import validators
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
    ingredient_name = SelectField("Surovina")
    category = QuerySelectField("Kategorie", query_factory=categories, allow_blank=True)

    is_vegetarian = BooleanField("Vegetariánské")
    is_vegan = BooleanField("Veganské")
    lactose_free = BooleanField("Bez laktózy")
    gluten_free = BooleanField("Bez lepku")

    submit = SubmitField("Filtrovat")

    def __init__(self, *args, ingredient_names=None, categories=None):
        if ingredient_names is None:
            raise Exception(
                f"{self.__class__.__name__} has no select (ingredient_names) values"
            )

        super().__init__(*args)
        self.set_ingredient_name(ingredient_names)

    def set_ingredient_name(self, ingredient_names):
        self.ingredient_name.choices = [name for name in ingredient_names]
