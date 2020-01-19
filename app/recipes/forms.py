from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField, FormField, FieldList, validators
from wtforms.fields.html5 import SearchField

from app.ingredients.forms import RecipeIngredientForm


class GetRecipesForm(FlaskForm):
    q = SearchField("Search", default="")
    no_name = BooleanField("Name", default=False)
    no_description = BooleanField("Description", default=False)
    no_steps = BooleanField("Steps", default=False)

    def toggle_filters(self):
        self.no_name.data = not self.no_name.data
        self.no_description.data = not self.no_description.data
        self.no_steps.data = not self.no_steps.data

    class Meta:
        csrf = False


class EditRecipeForm(FlaskForm):
    name = StringField("Name", default="")
    description = TextAreaField("Description", default="")
    steps = TextAreaField("Steps", default="")
    ingredient_amounts = FieldList(FormField(RecipeIngredientForm))

    class Meta:
        csrf = False
