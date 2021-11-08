import datetime

from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms import validators

from flask_wtf import FlaskForm


class EventsForm(FlaskForm):
    name = StringField(
        "Název akce", [validators.InputRequired("Název musí být vyplněn")]
    )

    date_from = DateField("Od", default=datetime.date.today())
    date_to = DateField(
        "Do", default=datetime.date.today() + datetime.timedelta(days=14)
    )

    people_count = IntegerField(
        "Počet lidí",
        [
            validators.InputRequired("Počet lidí musí být vyplněn"),
            validators.NumberRange(min=1),
        ],
    )

    submit = SubmitField("Přidat akci")
