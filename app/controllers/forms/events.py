from datetime import datetime, timedelta

from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.validators import InputRequired, NumberRange

from flask_wtf import FlaskForm


class EventsForm(FlaskForm):
    name = StringField("Název akce", [InputRequired("Název musí být vyplněn")])

    date_from = DateField("Od")
    date_to = DateField("Do")

    people_count = IntegerField(
        "Počet lidí",
        [
            InputRequired("Počet lidí musí být vyplněn"),
            NumberRange(min=1),
        ],
    )

    submit = SubmitField("Přidat akci")

    def __init__(self, formdata=None, obj=None, **kwargs):
        super().__init__(formdata=formdata, obj=obj, **kwargs)

        self.date_from.data = datetime.today()
        self.date_to.data = datetime.today() + timedelta(days=14)
