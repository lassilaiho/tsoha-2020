from decimal import Decimal
import re

from flask_wtf import FlaskForm
from wtforms import StringField, validators

from app.ingredients.models import Ingredient, RecipeIngredient

amount_pattern = re.compile(
    r"^(?P<value>\s*(\+|\-)?\d+((\.|,)\d+)?)(?P<unit>.*)$")


class RecipeIngredientForm(FlaskForm):
    amount = StringField("Amount", default="")
    name = StringField("Name", default="")

    @staticmethod
    def join_amount(value, unit):
        if value == 1:
            return unit
        else:
            return f"{value} {unit}"

    def parse_amount(self):
        match = amount_pattern.search(self.amount.data)
        if match:
            return Decimal(match.group("value")), match.group("unit").strip()
        else:
            return Decimal(1), self.amount.data.strip()

    class Meta:
        csrf = False
