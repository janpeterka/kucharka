from wtforms import StringField, SubmitField, IntegerField, HiddenField
from wtforms.validators import InputRequired, NumberRange

# from wtforms.widgets import TextArea

from flask_wtf import FlaskForm

from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField


def categories():
    from app.models.recipe_categories import RecipeCategory

    return RecipeCategory.load_all()


def measurements():
    from app.models.measurements import Measurement

    return Measurement.load_all()


def dietary_labels():
    from app.models.labels import Label

    return Label.load_dietary()


def difficulty_labels():
    from app.models.labels import Label

    return Label.load_by_category_name("difficulty")


class RecipesForm(FlaskForm):
    name = StringField("Název receptu", [InputRequired("Název musí být vyplněn")])

    # description = StringField("Popis", widget=TextArea())

    category = QuerySelectField("Kategorie", query_factory=categories, allow_blank=True)
    portion_count = IntegerField(
        "Počet porcí", [NumberRange(message="Musí být alespoň jedna porce", min=1)]
    )

    dietary_labels = QuerySelectMultipleField(
        "Dietní omezení", query_factory=dietary_labels
    )
    difficulty_label = QuerySelectField(
        "Obtížnost přípravy", query_factory=difficulty_labels, allow_blank=True
    )

    labels = HiddenField()

    submit = SubmitField("Přidat recept")

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
