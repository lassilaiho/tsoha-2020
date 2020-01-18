from sqlalchemy.sql import text

from app.main import db


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    recipes = db.relationship(
        "Recipe", backref="account", lazy=True,
        cascade="all, delete, delete-orphan")
    ingredients = db.relationship(
        "Ingredient", backref="account", lazy=True,
        cascade="all, delete, delete-orphan")
    shopping_list_items = db.relationship(
        "ShoppingListItem", backref="account", lazy=True,
        cascade="all, delete, delete-orphan")

    def __init__(self, username, password_hash, role):
        self.username = username
        self.password_hash = password_hash
        self.role = role

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def get_item_and_recipe_counts(account_id):
        stmt = text("""
SELECT COUNT(DISTINCT items.id), COUNT(DISTINCT recipes.id)
FROM accounts
LEFT JOIN shopping_list_items items ON items.account_id = accounts.id
LEFT JOIN recipes ON recipes.account_id = accounts.id
GROUP BY accounts.id
HAVING accounts.id = :account_id;
""").params(account_id=account_id)
        rows = db.session().execute(stmt)
        try:
            row = rows.fetchone()
            return row[0], row[1]
        finally:
            rows.close()
