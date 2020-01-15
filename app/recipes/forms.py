from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FormField, FieldList, validators

from app.ingredients.forms import RecipeIngredientForm


class EditRecipeForm(FlaskForm):
    name = StringField("Name", default="")
    description = TextAreaField("Description", default="")
    steps = TextAreaField("Steps", default="")
    ingredient_amounts = FieldList(FormField(RecipeIngredientForm))

    class Meta:
        csrf = False
