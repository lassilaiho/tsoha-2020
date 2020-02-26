from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, StringField, validators


class AddIngredientToShoppingListForm(FlaskForm):
    recipe_id = IntegerField(
        "Recipe ID", validators=[validators.input_required()])
    ingredient_id = IntegerField(
        "Ingredient ID", validators=[validators.input_required()])
    # The size of this field is not limited because it will be clamped to a
    # suitable range when needed.
    amount = FloatField("Amount", default=1.0)
    amount_unit = StringField(
        "Unit", [validators.length(max=5000)], default="")
