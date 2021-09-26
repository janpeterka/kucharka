from wtforms import SubmitField, SelectField, BooleanField

from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField


def categories():
    from app.models.recipe_categories import RecipeCategory

    return RecipeCategory.load_all()


class PublicRecipeFilterForm(FlaskForm):
    ingredient_name = SelectField("Surovina")
    category = QuerySelectField(
        "Kategorie", query_factory=categories, get_label="name", allow_blank=True
    )
    with_reaction = BooleanField("Moje oblíbené")

    is_vegetarian = BooleanField("Vegetariánské")
    is_vegan = BooleanField("Veganské")
    lactose_free = BooleanField("Bez laktózy")
    gluten_free = BooleanField("Bez lepku")

    submit = SubmitField("Filtrovat")

    def __init__(self, *args, ingredient_names=None):
        if ingredient_names is None:
            raise Exception(
                f"{self.__class__.__name__} has no select (ingredient_names) values"
            )

        super().__init__(*args)
        self.set_ingredient_name(ingredient_names)

    def set_ingredient_name(self, ingredient_names):
        self.ingredient_name.choices = [name for name in ingredient_names]
