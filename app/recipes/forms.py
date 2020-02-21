from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField, FormField, FieldList, IntegerField, validators
from wtforms.fields.html5 import SearchField

from app.ingredients.forms import RecipeIngredientForm


class GetRecipesForm(FlaskForm):
    q = SearchField("Search", [validators.length(
        max=5000,
        message="Search text can be at most %(max)d characters",
    )], default="")
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
    name = StringField("Name", [
        validators.data_required("Name must not be empty"),
        validators.length(max=5000),
    ])
    description = TextAreaField(
        "Description", [validators.length(max=5000)], default="")
    steps = TextAreaField("Steps", [validators.length(max=5000)], default="")
    ingredient_amounts = FieldList(
        FormField(RecipeIngredientForm),
        validators=[validators.length(
            max=100,
            message="Recipe can have at most %(max)d ingredients.",
        )],
    )
