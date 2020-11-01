from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField, FormField, FieldList, IntegerField, validators
from wtforms.fields.html5 import SearchField

from app.ingredients.forms import RecipeIngredientForm


class GetRecipesForm(FlaskForm):
    query = SearchField("Search", [validators.length(
        max=5000,
        message="Search text can be at most %(max)d characters",
    )], default="")
    page = IntegerField("Page", default=1)

    # The filter fields are defined as negatives (e.g. no_name instead of name)
    # to set proper defaults when some filters are unchecked. Browsers don't
    # send unchecked boolean fields, so it is impossible to determine whether a
    # field is absent or unchecked. We want the default behavior to be checked,
    # so negating the field definition makes the absence of a field equivalent
    # to an unchecked field.
    no_name = BooleanField("Name", default=False)
    no_description = BooleanField("Description", default=False)
    no_steps = BooleanField("Steps", default=False)

    def toggle_filters(self):
        self.no_name.data = not self.no_name.data
        self.no_description.data = not self.no_description.data
        self.no_steps.data = not self.no_steps.data

    def page_clamped(self, min_value=1, max_value=9999999):
        return max(min_value, min(self.page.data, max_value))

    class Meta:
        # CSRF protection isn't needed because this form is only used in GET
        # requests.
        csrf = False


class GroupedRecipeIngredientForm(RecipeIngredientForm):
    group = StringField("Group", [validators.length(max=5000)], default="")


class EditRecipeForm(FlaskForm):
    name = StringField("Name", [
        validators.data_required("Name must not be empty"),
        validators.length(max=5000),
    ])
    description = TextAreaField(
        "Description", [validators.length(max=5000)], default="")
    steps = TextAreaField("Steps", [validators.length(max=5000)], default="")
    ingredient_amounts = FieldList(
        FormField(GroupedRecipeIngredientForm),
        validators=[validators.length(
            max=100,
            message="Recipe can have at most %(max)d ingredients.",
        )],
    )
