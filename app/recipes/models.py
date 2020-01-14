from app.main import db


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    steps = db.Column(db.String(), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey(
        "accounts.id"), nullable=False)

    def __init__(self, name, description, steps):
        self.name = name
        self.description = description
        self.steps = steps
