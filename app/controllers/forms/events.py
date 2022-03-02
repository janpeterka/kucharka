from datetime import datetime, timedelta

from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.validators import InputRequired, NumberRange

from flask_wtf import FlaskForm


class EventsForm(FlaskForm):
    name = StringField("název akce", [InputRequired("název musí být vyplněn")])

    date_from = DateField("od")
    date_to = DateField("do")

    people_count = IntegerField(
        "počet lidí",
        [
            InputRequired("počet lidí musí být vyplněn"),
            NumberRange(min=1),
        ],
    )

    submit = SubmitField("Přidat akci")

    def __init__(self, formdata=None, obj=None, **kwargs):
        super().__init__(formdata=formdata, obj=obj, **kwargs)

        if not self.date_from.data:
            self.date_from.data = datetime.now()
        if not self.date_to.data:
            self.date_to.data = datetime.now() + timedelta(days=14)
