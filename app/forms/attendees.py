from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired

from flask_wtf import FlaskForm

from wtforms_sqlalchemy.fields import QuerySelectMultipleField

# from app.helpers.form_select_field import ExtendedSelectWidget


def dietary_labels():
    from app.models.labels import Label

    return Label.load_dietary()


class AttendeeForm(FlaskForm):
    name = StringField("jméno", [InputRequired("jméno musí být vyplněno")])

    portion_size_ratio = SelectField(
        "velikost porce", choices=[(1, "normální porce"), (0.8, "malá porce (80%)")]
    )
    labels = QuerySelectMultipleField("dietní omezení", query_factory=dietary_labels)

    submit = SubmitField("přidat")
    update = SubmitField("upravit")

    # def __init__(self, formdata=None, obj=None, **kwargs):
    # super().__init__(formdata=formdata, obj=obj, **kwargs)
    # self.set_labels()

    # def set_dietary_labels(self):
    #     from app.models.labels import Label

    #     option_attr = {
    #         f"dietary_labels-{i}": {"data-color": label.color}
    #         for i, label in enumerate(Label.load_dietary())
    #     }

    #     self.dietary_labels.option_attr = option_attr
