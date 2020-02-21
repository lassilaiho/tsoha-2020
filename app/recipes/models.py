from sqlalchemy.sql import text, func

from app.main import db
from app.ingredients.models import Ingredient, RecipeIngredient


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    steps = db.Column(db.Text(), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey(
        "accounts.id"), nullable=False, index=True)

    ingredient_amounts = db.relationship(
        "RecipeIngredient", backref="recipe", lazy=True,
        cascade="all, delete, delete-orphan")

    def __init__(self, name, description, steps):
        self.name = name
        self.description = description
        self.steps = steps

    def get_ingredients(self):
        stmt = text("""
SELECT ri.amount AS amount, ri.amount_unit AS amount_unit, i.id AS id, i.name AS name
FROM ingredients i, recipe_ingredient ri
WHERE
    ri.recipe_id = :recipe_id
    AND i.account_id = :account_id
    AND ri.ingredient_id = i.id
""").bindparams(recipe_id=self.id, account_id=self.account_id)
        return db.session().execute(stmt)

    def get_shopping_list_amounts(self):
        stmt = text("""
SELECT
    i.id AS id,
    SUM(sli.amount) AS amount,
    sli.amount_unit AS unit
FROM (
    SELECT DISTINCT
        i.id AS id,
        i.name AS name
    FROM ingredients i, recipe_ingredient ri
    WHERE
        i.account_id = :account_id
        AND i.id = ri.ingredient_id
        AND ri.recipe_id = :recipe_id
) i
LEFT JOIN shopping_list_items sli
ON sli.ingredient_id = i.id
WHERE sli.account_id = :account_id
GROUP BY i.id, sli.amount_unit
""").bindparams(recipe_id=self.id, account_id=self.account_id)
        return db.session().execute(stmt)

    def insert_ingredients_from_form(self, form):
        ingredients = []
        missing_ingredients = []
        ingredients_by_name = {}
        for recipe_ingredient_form in form.ingredient_amounts:
            name = recipe_ingredient_form.data["name"].strip()
            lower_name = name.lower()
            x = ingredients_by_name.get(lower_name)
            if not x:
                x = Ingredient.query.filter(
                    Ingredient.account_id == self.account_id,
                    func.lower(Ingredient.name) == lower_name,
                ).first()
                if not x:
                    x = Ingredient(name)
                    x.account_id = self.account_id
                    missing_ingredients.append(x)
                ingredients_by_name[lower_name] = x
            ingredients.append(x)
        db.session().bulk_save_objects(missing_ingredients, return_defaults=True)
        db.session().flush()

        recipe_ingredients = []
        for i, recipe_ingredient_form in enumerate(form.ingredient_amounts):
            amount, unit = recipe_ingredient_form.parse_amount()
            recipe_ingredients.append(RecipeIngredient(
                amount=amount,
                amount_unit=unit,
                ingredient_id=ingredients[i].id,
                recipe_id=self.id,
            ))
        db.session().bulk_save_objects(recipe_ingredients)
        db.session().flush()
