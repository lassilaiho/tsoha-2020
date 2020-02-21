from decimal import Decimal

from flask import render_template, request, abort, redirect, url_for
from flask_login import current_user
from sqlalchemy.orm import joinedload

from app.main import app, db, login_required
from app.shopping_list.models import ShoppingListItem
from app.shopping_list.forms import AddIngredientToShoppingListForm
from app.ingredients.models import Ingredient
from app.ingredients.forms import RecipeIngredientForm, clamp_amount


def render_shopping_list(form=None, form_id=None):
    item_query = ShoppingListItem.query.filter_by(
        account_id=current_user.id,
    ).options(joinedload(ShoppingListItem.ingredient))
    items = []
    incorrect_index = -1
    for i, item in enumerate(item_query):
        if form_id == item.id:
            incorrect_index = i
            items.append({
                "id": item.id,
                "amount": form.amount.data,
                "amount_errors": form.amount.errors,
                "name": form.name.data,
                "name_errors": form.name.errors,
            })
        else:
            name = item.ingredient.name
            if not name.strip():
                name = "\u00A0"
            items.append({
                "id": item.id,
                "amount": RecipeIngredientForm.join_amount(
                    item.amount,
                    item.amount_unit,
                ),
                "amount_errors": [],
                "name": name,
                "name_errors": [],
            })
    return render_template(
        "shopping_list/index.html",
        items=items,
        new_form=form if form_id == "new" else None,
        incorrect_index=incorrect_index,
    )


@app.route("/shopping-list")
@login_required
def get_shopping_list():
    return render_shopping_list()


@app.route("/shopping-list/new", methods=["POST"])
@login_required
def create_shopping_list_item():
    form = RecipeIngredientForm(request.form)
    if not form.validate():
        return render_shopping_list(form, "new")
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
        return render_shopping_list(form, item_id)
    item = ShoppingListItem.query.filter_by(
        id=item_id,
        account_id=current_user.id,
    ).first_or_404()
    item.amount, item.amount_unit = form.parse_amount()
    ingredient = Ingredient.insert_if_missing(
        form.name.data.strip(), current_user.id)
    item.ingredient_id = ingredient.id
    db.session().flush()
    Ingredient.delete_unused_ingredients(current_user.id)
    db.session().commit()
    return redirect(url_for("get_shopping_list"))


@app.route("/shopping-list/add", methods=["POST"])
@login_required
def add_ingredient_to_shopping_list():
    form = AddIngredientToShoppingListForm()
    if not form.validate():
        abort(400)
    item = ShoppingListItem.query.filter_by(
        account_id=current_user.id,
        ingredient_id=form.ingredient_id.data,
        amount_unit=form.amount_unit.data,
    ).first()
    if item is None:
        db.session().add(ShoppingListItem(
            amount=Decimal(clamp_amount(form.amount.data)),
            amount_unit=form.amount_unit.data,
            ingredient_id=form.ingredient_id.data,
            account_id=current_user.id,
        ))
    else:
        item.amount = clamp_amount(
            item.amount+Decimal(clamp_amount(form.amount.data)))
    db.session().commit()
    return redirect(url_for("get_recipe", recipe_id=form.recipe_id.data))


@app.route("/shopping-list/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_shopping_list_item(item_id: int):
    delete_count = ShoppingListItem.query.filter_by(
        id=item_id,
        account_id=current_user.id,
    ).delete()
    db.session().flush()
    Ingredient.delete_unused_ingredients(current_user.id)
    db.session().commit()
    return redirect(url_for("get_shopping_list"))
