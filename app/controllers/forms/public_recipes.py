from wtforms import SubmitField, BooleanField

from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField


def categories():
    from app.models.recipe_categories import RecipeCategory

    return RecipeCategory.load_all()


def dietary_labels():
    from app.models.labels import Label

    return Label.load_dietary()


def public_ingredients():
    from app.models.ingredients import Ingredient

    return Ingredient.load_all_in_public_recipes()


class PublicRecipeFilterForm(FlaskForm):
    ingredient = QuerySelectField(
        "Surovina", query_factory=public_ingredients, allow_blank=True
    )
    category = QuerySelectField("Kategorie", query_factory=categories, allow_blank=True)
    with_reaction = BooleanField("Moje oblíbené")

    with_labels = QuerySelectMultipleField(
        "Dietní omezení", query_factory=dietary_labels
    )

    submit = SubmitField("Filtrovat")
