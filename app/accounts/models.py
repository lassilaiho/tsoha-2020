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
