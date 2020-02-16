from flask import render_template
from flask_login import current_user

from app.main import app, login_required
from app.accounts.models import Account


@app.route("/")
@login_required
def index():
    item_count, recipe_count = \
        Account.get_item_and_recipe_counts(current_user.id)
    return render_template(
        "index.html",
        item_count=item_count,
        recipe_count=recipe_count,
    )
