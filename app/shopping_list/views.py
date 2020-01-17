from flask import render_template, request, abort, redirect, url_for
from flask_login import login_required, current_user

from app.main import app, db
from app.shopping_list.models import ShoppingListItem
from app.ingredients.models import Ingredient
from app.ingredients.forms import RecipeIngredientForm


@app.route("/shopping-list")
@login_required
def get_shopping_list():
    items = []
    for item in current_user.shopping_list_items:
        name = item.ingredient.name
        if not name.strip():
            name = "\u00A0"
        items.append({
            "id": item.id,
            "amount": RecipeIngredientForm.join_amount(
                item.amount,
                item.amount_unit,
            ),
            "name": name,
        })
    return render_template(
        "shopping_list/index.html",
        items=items,
    )


@app.route("/shopping-list/new", methods=["POST"])
@login_required
def create_shopping_list_item():
    form = RecipeIngredientForm(request.form)
    if not form.validate():
        abort(400)
    item = ShoppingListItem()
    item.amount, item.amount_unit = form.parse_amount()
    item.account_id = current_user.id
    ingredient = Ingredient.insert_if_missing(form.name.data, current_user.id)
    item.ingredient_id = ingredient.id
    db.session().add(item)
    db.session().commit()
    return redirect(url_for("get_shopping_list"))


@app.route("/shopping-list/<int:item_id>", methods=["POST"])
@login_required
def update_shopping_list_item(item_id: int):
    form = RecipeIngredientForm(request.form)
    if not form.validate():
        abort(400)
    item = ShoppingListItem.query.filter_by(
        id=item_id,
        account_id=current_user.id,
    ).first()
    if not item:
        abort(404)
    item.amount, item.amount_unit = form.parse_amount()
    ingredient = Ingredient.insert_if_missing(
        form.name.data.strip(), current_user.id)
    item.ingredient_id = ingredient.id
    db.session().flush()
    Ingredient.delete_unused_ingredients(current_user.id)
    db.session().commit()
    return redirect(url_for("get_shopping_list"))


@app.route("/shopping-list/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_shopping_list_item(item_id: int):
    item = ShoppingListItem.query.filter_by(
        id=item_id,
        account_id=current_user.id,
    ).first()
    if item is None:
        abort(404)
    db.session().delete(item)
    db.session().flush()
    Ingredient.delete_unused_ingredients(current_user.id)
    db.session().commit()
    return redirect(url_for("get_shopping_list"))
