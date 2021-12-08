from flask_wtf import FlaskForm

from wtforms.fields import SubmitField
from flask_wtf.file import FileField


class PhotoForm(FlaskForm):
    file = FileField("Fotka")
    submit = SubmitField("Nahrát")
