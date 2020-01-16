from sqlalchemy.sql import text

from app.main import db


class Ingredient(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey(
        "accounts.id"), nullable=False)

    ingredient_amounts = db.relationship(
        "RecipeIngredient", backref="ingredient", lazy=True,
        cascade="all, delete, delete-orphan")

    def __init__(self, name):
        self.name = name

    @staticmethod
    def delete_unused_ingredients(account_id):
        stmt = text("""
DELETE FROM ingredients
WHERE ingredients.id IN (
    SELECT ingredients.id
    FROM ingredients
    LEFT JOIN recipe_ingredient
    ON recipe_ingredient.ingredient_id = ingredients.id
    WHERE ingredients.account_id = :account_id
    GROUP BY ingredients.id
    HAVING COUNT(recipe_ingredient.id) = 0
)""").params(account_id=account_id)
        db.session().execute(stmt)

    @staticmethod
    def insert_if_missing(name, account_id):
        x = Ingredient.query.filter(Ingredient.name.ilike(name)).first()
        if x:
            return x
        x = Ingredient(name)
        x.account_id = account_id
        db.session().add(x)
        db.session().flush()
        return x


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredient"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric, nullable=False)
    amount_unit = db.Column(db.String, nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey(
        "ingredients.id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        "recipes.id"), nullable=False)

    @staticmethod
    def insert(amount, amount_unit, ingredient_id, recipe_id):
        x = RecipeIngredient(
            amount=amount,
            amount_unit=amount_unit,
            ingredient_id=ingredient_id,
            recipe_id=recipe_id,
        )
        db.session().add(x)
        db.session().flush()
        return x
