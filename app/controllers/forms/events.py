import datetime

from wtforms import StringField, SubmitField, IntegerField
from wtforms import validators

from flask_wtf import FlaskForm

from wtforms.widgets import TextArea
from wtforms.fields.html5 import DateField


class EventsForm(FlaskForm):
    name = StringField(
        "Název akce", [validators.InputRequired("Název musí být vyplněn")]
    )

    description = StringField("Popis", widget=TextArea())

    date_from = DateField("Od", default=datetime.date.today())
    date_to = DateField(
        "Do", default=datetime.date.today() + datetime.timedelta(days=14)
    )

    people_count = IntegerField("Počet lidí")

    submit = SubmitField("Přidat akci")
