from wtforms import StringField, SubmitField, SelectField, IntegerField, BooleanField
from wtforms import validators
from wtforms.widgets import TextArea

from flask_wtf import FlaskForm


class RecipesForm(FlaskForm):
    name = StringField(
        "Název receptu", [validators.InputRequired("Název musí být vyplněn")]
    )

    description = StringField("Popis", widget=TextArea())

    category = SelectField("Kategorie", coerce=int)
    portion_count = IntegerField("Počet porcí", [validators.NumberRange(min=1)])

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
    category = SelectField("Kategorie", coerce=int)

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
        if categories is None:
            raise Exception(
                f"{self.__class__.__name__} has no select (categories) values"
            )

        super().__init__(*args)
        self.set_ingredient_name(ingredient_names)
        self.set_category(categories)

    def set_ingredient_name(self, ingredient_names):
        self.ingredient_name.choices = [name for name in ingredient_names]

    def set_category(self, categories):
        self.category.choices = [
            (category.id, category.name) for category in categories
        ]
