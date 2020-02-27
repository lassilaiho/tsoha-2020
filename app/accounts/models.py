from sqlalchemy.sql import text, exists

from app.main import db


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False)

    valid_roles = {"user", "admin"}

    recipes = db.relationship(
        "Recipe", backref="account", lazy=True,
        passive_deletes=True)
    ingredients = db.relationship(
        "Ingredient", backref="account", lazy=True,
        passive_deletes=True)
    shopping_list_items = db.relationship(
        "ShoppingListItem", backref="account", lazy=True,
        passive_deletes=True)

    def is_admin(self):
        return self.role == "admin"

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def fullfills_role(self, role):
        """
        Checks if this Account fullfills `role`.

        The role "user" is fullfilled by roles "user" and "admin". The role
        "admin" is fullfilled by role "admin".
        """
        if self.role == role:
            return True
        return self.role == "admin" and role == "user"

    @staticmethod
    def get_top_recipe_collectors(count):
        stmt = text("""
SELECT accounts.username username, COUNT(recipes.id) recipe_count
FROM accounts
LEFT JOIN recipes ON recipes.account_id = accounts.id
GROUP BY accounts.username
ORDER BY COUNT(recipes.id) DESC, accounts.username
LIMIT :count
""").params(count=count)
        rows = db.session().execute(stmt)
        try:
            return rows.fetchall()
        finally:
            rows.close()

    @staticmethod
    def is_username_taken(username):
        return db.session().query(
            exists().where(Account.username == username)).scalar()
