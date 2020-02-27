from flask import request, jsonify
from flask_login import current_user
from sqlalchemy.sql.expression import select

from app.main import app, db, login_required
from app.ingredients.models import Ingredient


@app.route("/ingredients/completions")
@login_required
def ingredient_completions():
    query = request.args.get("query", "")
    try:
        count = int(request.args.get("count", "10"))
        if count <= 0:
            raise ValueError()
    except ValueError:
        return jsonify(error="Query parameter 'count' must be a natural number."), 400
    completions = db.session().execute(select(
        columns=[Ingredient.name],
        from_obj=Ingredient,
        whereclause=(Ingredient.account_id == current_user.id) &
        Ingredient.name.contains(query),
        distinct=True,
    ).limit(count))
    return jsonify(completions=[completion[0] for completion in completions])
