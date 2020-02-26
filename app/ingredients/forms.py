from decimal import Decimal, InvalidOperation
import re

from flask_wtf import FlaskForm
from wtforms import StringField, validators, ValidationError

from app.ingredients.models import Ingredient, RecipeIngredient

amount_pattern = re.compile(
    r"^(?P<value>\s*(\+|\-)?\d+((\.|,)\d+)?)(?P<unit>.*)$")


def parse_amount(amount):
    match = amount_pattern.search(amount)
    if match:
        value = match.group("value").replace(",", ".")
        return Decimal(clamp_amount(value)), match.group("unit").strip()
    else:
        return Decimal(1), amount.strip()


def validate_amount_value(min=0, max=9999999):
    def validate(form, field):
        try:
            value, unit = parse_amount(field.data)
        except InvalidOperation:
            raise ValidationError("Invalid amount.")
        if value > max:
            raise ValidationError(f"Amount can be at most {max}")
        if value < min:
            raise ValidationError(f"Amount must be at least {min}")
    return validate


def clamp_amount(amount, min=0, max=9999999):
    if amount < min:
        return min
    if amount > max:
        return max
    return amount


class RecipeIngredientForm(FlaskForm):
    amount = StringField("Amount", [
        validators.length(max=5000),
        validate_amount_value(),
    ], default="")
    name = StringField("Name", [validators.length(max=5000)], default="")

    @staticmethod
    def join_amount(value, unit):
        value = Decimal(value)
        if value == value.to_integral():
            value = value.quantize(Decimal(1))
        else:
            value = value.normalize()
        if unit:
            return f"{value} {unit}"
        return str(value)

    def parse_amount(self):
        return parse_amount(self.amount.data)
