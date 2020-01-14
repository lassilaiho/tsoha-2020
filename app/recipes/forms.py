from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators


class EditRecipeForm(FlaskForm):
    name = StringField("Name", default="")
    description = TextAreaField("Description", default="")
    steps = TextAreaField("Steps", default="")

    class Meta:
        csrf = False
