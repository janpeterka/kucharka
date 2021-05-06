from wtforms import SubmitField, SelectField, BooleanField

from flask_wtf import FlaskForm


class PublicRecipeFilterForm(FlaskForm):
    ingredient_name = SelectField("Surovina")
    category = SelectField("Kategorie", coerce=int)
    with_reaction = BooleanField("Moje oblíbené")

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
