from wtforms import StringField, SubmitField, IntegerField, HiddenField
from wtforms.validators import InputRequired, NumberRange

# from wtforms.widgets import TextArea

from flask_wtf import FlaskForm

from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from app.helpers.form_select_field import ExtendedSelectWidget


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

    return Label.load_difficulty()


class RecipesForm(FlaskForm):
    name = StringField("název receptu", [InputRequired("název musí být vyplněn")])

    # description = StringField("Popis", widget=TextArea())

    category = QuerySelectField("kategorie", query_factory=categories, allow_blank=True)
    portion_count = IntegerField(
        "počet porcí", [NumberRange(message="musí být alespoň jedna porce", min=1)]
    )

    dietary_labels = QuerySelectMultipleField(
        "dietní omezení",
        query_factory=dietary_labels,
        widget=ExtendedSelectWidget(multiple=True),
    )

    difficulty_label = QuerySelectField(
        "obtížnost přípravy",
        query_factory=difficulty_labels,
        allow_blank=True,
        widget=ExtendedSelectWidget(),
    )

    labels = HiddenField()

    submit = SubmitField("přidat recept")

    def __init__(self, formdata=None, obj=None, **kwargs):
        super().__init__(formdata=formdata, obj=obj, **kwargs)
        self.set_labels()
        self.set_difficulty_label()
        self.set_dietary_labels()

    def set_dietary_labels(self):
        from app.models.labels import Label

        option_attr = {
            f"dietary_labels-{i}": {"data-color": label.color}
            for i, label in enumerate(Label.load_dietary())
        }

        self.dietary_labels.option_attr = option_attr

    def set_difficulty_label(self):
        from app.models.labels import Label

        option_attr = {
            f"difficulty_label-{i+1}": {"data-color": label.color}
            for i, label in enumerate(Label.load_difficulty())
        }

        self.difficulty_label.option_attr = option_attr

    def set_labels(self):
        from app.models.label_categories import LabelCategory

        self.labels.data = []

        for category in LabelCategory.load_all():
            if category.allow_multiple:
                attr_name = f"{category.name}_labels"
            else:
                attr_name = f"{category.name}_label"

            field = getattr(self, attr_name, None)
            if field:
                specific_labels = field.data
                if not specific_labels:
                    continue
                elif type(specific_labels) == list:
                    self.labels.data.extend(specific_labels)
                else:
                    self.labels.data.append(specific_labels)
