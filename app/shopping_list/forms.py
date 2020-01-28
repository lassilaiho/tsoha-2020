from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, TextField, validators


class AddIngredientToShoppingListForm(FlaskForm):
    recipe_id = IntegerField(validators=[validators.input_required()])
    ingredient_id = IntegerField(validators=[validators.input_required()])
    amount = FloatField(default=1.0)
    amount_unit = TextField(default="")
