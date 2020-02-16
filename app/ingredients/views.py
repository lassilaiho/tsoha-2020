from flask import request, jsonify
from flask_login import current_user
from sqlalchemy.sql.expression import select

from app.main import app, db, login_required
from app.ingredients.models import Ingredient


@app.route("/ingredients/completions")
@login_required
def ingredient_completions():
    q = request.args.get("q", "")
    try:
        count = int(request.args.get("c", "10"))
        if count <= 0:
            raise ValueError()
    except ValueError:
        return jsonify(error="Query parameter 'c' must be a natural number."), 400
    completions = db.session().execute(select(
        columns=[Ingredient.name],
        from_obj=Ingredient,
        whereclause=(Ingredient.account_id == current_user.id) &
        Ingredient.name.contains(q),
        distinct=True,
    ).limit(count))
    result = []
    for x in completions:
        result.append(x[0])
    return jsonify(completions=result)
