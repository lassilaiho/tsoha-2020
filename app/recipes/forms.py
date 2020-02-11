from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField, FormField, FieldList, IntegerField, validators
from wtforms.fields.html5 import SearchField

from app.ingredients.forms import RecipeIngredientForm


class GetRecipesForm(FlaskForm):
    q = SearchField("Search", default="")
    p = IntegerField("Page", default=1)
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
    name = StringField(
        "Name", [validators.data_required("Name must not be empty")])
    description = TextAreaField("Description", default="")
    steps = TextAreaField("Steps", default="")
    ingredient_amounts = FieldList(FormField(RecipeIngredientForm))
