from decimal import Decimal
import re

from flask_wtf import FlaskForm
from wtforms import StringField, validators

from app.ingredients.models import Ingredient, RecipeIngredient

amount_pattern = re.compile(
    r"^(?P<value>\s*(\+|\-)?\d+((\.|,)\d+)?)(?P<unit>.*)$")


class RecipeIngredientForm(FlaskForm):
    amount = StringField("Amount", default="")
    name = StringField("Name", [validators.required()])

    @staticmethod
    def join_amount(value, unit):
        if value == 1:
            return unit
        else:
            return f"{value} {unit}"

    def parse_data_to(self, ingredient, recipe_ingredient):
        ingredient.name = self.name.data
        match = amount_pattern.search(self.amount.data)
        if match:
            recipe_ingredient.amount = Decimal(match.group("value"))
            recipe_ingredient.amount_unit = match.group("unit").strip()
        else:
            recipe_ingredient.amount = Decimal(1)
            recipe_ingredient.amount_unit = self.amount.data.strip()

    class Meta:
        csrf = False
