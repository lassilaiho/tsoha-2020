from app.main import db


class ShoppingListItem(db.Model):
    __tablename__ = "shopping_list_items"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric, nullable=False)
    amount_unit = db.Column(db.Text, nullable=False)
    ingredient_id = db.Column(
        db.Integer, db.ForeignKey(
            "ingredients.id",
            ondelete="CASCADE",
        ), nullable=False, index=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey(
            "accounts.id",
            ondelete="CASCADE",
        ), nullable=False, index=True)
