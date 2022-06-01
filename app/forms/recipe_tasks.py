from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea


class RecipeTaskForm(FlaskForm):
    name = StringField("název", [InputRequired("název musí být vyplněn")])
    description = StringField("popis", widget=TextArea())
    days_before_cooking = IntegerField("dny před vařením", default=0)

    submit = SubmitField("přidat úkol")
