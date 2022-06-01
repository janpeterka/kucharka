from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea


class DailyPlanTaskForm(FlaskForm):
    name = StringField("název", [InputRequired("název musí být vyplněn")])
    description = StringField("popis", widget=TextArea())

    submit = SubmitField("přidat úkol")
