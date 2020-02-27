from sqlalchemy.sql import text, func

from app.main import db


class Ingredient(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey(
        "accounts.id",
        ondelete="CASCADE",
    ), nullable=False)

    ingredient_amounts = db.relationship(
        "RecipeIngredient", backref="ingredient", lazy=True,
        passive_deletes=True)
    shopping_list_items = db.relationship(
        "ShoppingListItem", backref="ingredient", lazy=True,
        passive_deletes=True)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def delete_unused_ingredients(account_id):
        stmt = text("""
DELETE FROM ingredients
WHERE ingredients.id IN (
    SELECT i.id FROM ingredients i
    LEFT JOIN recipe_ingredient ri ON ri.ingredient_id = i.id
    LEFT JOIN shopping_list_items sli ON sli.ingredient_id = i.id
    WHERE
        i.account_id = :account_id
        AND ri.id IS NULL
        AND sli.id IS NULL
)""").params(account_id=account_id)
        db.session().execute(stmt)

    @staticmethod
    def insert_if_missing(name, account_id):
        ingredient = Ingredient.query.filter(
            Ingredient.account_id == account_id,
            func.lower(Ingredient.name) == func.lower(name),
        ).first()
        if ingredient:
            return ingredient
        ingredient = Ingredient(name)
        ingredient.account_id = account_id
        db.session().add(ingredient)
        db.session().flush()
        return ingredient


idx_ingredient_account_id_name_lower = db.Index(
    "idx_ingredient_account_id_name_lower",
    Ingredient.account_id,
    func.lower(Ingredient.name),
)


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredient"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric, nullable=False)
    amount_unit = db.Column(db.Text, nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey(
        "ingredients.id",
        ondelete="CASCADE",
    ), nullable=False, index=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        "recipes.id",
        ondelete="CASCADE",
    ), nullable=False, index=True)
