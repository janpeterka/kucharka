from wtforms import SubmitField, BooleanField, HiddenField, StringField, SelectField

from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField


def categories():
    from app.models.recipe_categories import RecipeCategory

    return RecipeCategory.load_all()


def dietary_labels():
    from app.models.labels import Label

    return Label.load_dietary()


def difficulty_labels():
    from app.models.labels import Label

    return Label.load_by_category_name("difficulty")


def public_ingredients():
    from app.models.ingredients import Ingredient

    return Ingredient.load_all_in_public_recipes()


class PublicRecipeFilterForm(FlaskForm):
    ingredient = QuerySelectField(
        "obsahuje surovinu", query_factory=public_ingredients, allow_blank=True
    )
    category = QuerySelectField("kategorie", query_factory=categories, allow_blank=True)
    with_reaction = BooleanField("moje oblíbené")
    favorite = SelectField("jenom oblíbené?", choices=[("0", ""), ("1", "ano")])
    sort_by = SelectField(
        "seřadit",
        choices=[("reactions", "oblíbenost"), ("name", "jméno"), ("author", "autor")],
    )

    dietary_labels = QuerySelectMultipleField(
        "dietní omezení", query_factory=dietary_labels
    )
    difficulty_labels = QuerySelectMultipleField(
        "obtížnost přípravy", query_factory=difficulty_labels
    )
    name = StringField("název")

    labels = HiddenField()

    submit = SubmitField("filtrovat")
