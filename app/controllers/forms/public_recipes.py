from wtforms import SubmitField, BooleanField, HiddenField

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

    dietary_labels = QuerySelectMultipleField(
        "Dietní omezení", query_factory=dietary_labels
    )

    labels = HiddenField()

    submit = SubmitField("Filtrovat")

    def set_labels(form):
        from app.models.label_categories import LabelCategory

        form.labels.data = []

        for category in LabelCategory.load_all():
            if category.allow_multiple:
                attr_name = f"{category.name}_labels"
            else:
                attr_name = f"{category.name}_label"

            field = getattr(form, attr_name, None)
            if field:
                specific_labels = field.data
                if not specific_labels:
                    continue
                elif type(specific_labels) == list:
                    form.labels.data.extend(specific_labels)
                else:
                    form.labels.data.append(specific_labels)
