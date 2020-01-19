from flask import render_template, url_for, redirect, request, abort
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import false

from app.main import app, db
from app.recipes.models import Recipe
from app.recipes.forms import EditRecipeForm, GetRecipesForm
from app.ingredients.models import Ingredient, RecipeIngredient
from app.ingredients.forms import RecipeIngredientForm


def render_edit_form(action, form):
    return render_template(
        "recipes/edit.html",
        form_action=action,
        form=form,
    )


@app.route("/recipes")
@login_required
def get_recipes():
    form = GetRecipesForm(request.args)
    if not form.validate():
        abort(400)
    if form.q.data == "":
        recipes = Recipe.query.filter_by(account_id=current_user.id)
    else:
        filter = false()
        if not form.no_name.data:
            filter |= Recipe.name.contains(form.q.data, autoescape=True)
        if not form.no_description.data:
            filter |= Recipe.description.contains(form.q.data, autoescape=True)
        if not form.no_steps.data:
            filter |= Recipe.steps.contains(form.q.data, autoescape=True)
        filter &= Recipe.account_id == current_user.id
        recipes = Recipe.query.filter(filter)
    form.toggle_filters()
    return render_template(
        "recipes/index.html",
        recipes=recipes.order_by(Recipe.name).all(),
        form=form,
    )


@app.route("/recipes/new")
@login_required
def create_recipe_form():
    return render_edit_form(url_for("create_recipe"), EditRecipeForm())


@app.route("/recipes/new", methods=["POST"])
@login_required
def create_recipe():
    form = EditRecipeForm(request.form)
    if not form.validate():
        return render_edit_form(url_for("create_recipe"), form)
    recipe = Recipe(
        name=form.name.data,
        description=form.description.data,
        steps=form.steps.data,
    )
    recipe.account_id = current_user.id
    db.session().add(recipe)
    db.session().flush()
    for recipe_ingredient_form in form.ingredient_amounts:
        ingredient = Ingredient.insert_if_missing(
            recipe_ingredient_form.data["name"].strip(), current_user.id)
        amount, unit = recipe_ingredient_form.parse_amount()
        RecipeIngredient.insert(amount, unit, ingredient.id, recipe.id)
    db.session().commit()
    return redirect(url_for("get_recipes"))


@app.route("/recipes/<int:recipe_id>")
@login_required
def get_recipe(recipe_id: int):
    recipe = Recipe.query.filter_by(
        id=recipe_id,
        account_id=current_user.id,
    ).first()
    if recipe is None:
        abort(404)
    form = EditRecipeForm()
    form.name.data = recipe.name
    form.description.data = recipe.description
    form.steps.data = recipe.steps
    for recipe_ingredient in recipe.ingredient_amounts:
        form.ingredient_amounts.append_entry({
            "name": recipe_ingredient.ingredient.name,
            "amount": RecipeIngredientForm.join_amount(
                recipe_ingredient.amount,
                recipe_ingredient.amount_unit,
            ),
        })
    return render_edit_form(
        url_for("update_recipe", recipe_id=recipe_id),
        form,
    )


@app.route("/recipes/<int:recipe_id>", methods=["POST"])
@login_required
def update_recipe(recipe_id: int):
    form = EditRecipeForm(request.form)
    if not form.validate():
        return render_edit_form(
            url_for("update_recipe", recipe_id=recipe_id),
            form,
        )
    recipe = Recipe.query.filter_by(
        id=recipe_id,
        account_id=current_user.id,
    ).first()
    if recipe is None:
        abort(404)
    for x in RecipeIngredient.query.filter_by(recipe_id=recipe.id):
        db.session().delete(x)
    db.session.flush()
    recipe.name = form.name.data
    recipe.description = form.description.data
    recipe.steps = form.steps.data
    for recipe_ingredient_form in form.ingredient_amounts:
        ingredient = Ingredient.insert_if_missing(
            recipe_ingredient_form.data["name"].strip(), current_user.id)
        amount, unit = recipe_ingredient_form.parse_amount()
        RecipeIngredient.insert(amount, unit, ingredient.id, recipe.id)
    Ingredient.delete_unused_ingredients(current_user.id)
    db.session().commit()
    return redirect(url_for("get_recipes"))


@app.route("/recipes/<int:recipe_id>/delete", methods=["POST"])
@login_required
def delete_recipe(recipe_id: int):
    recipe = Recipe.query.filter_by(
        id=recipe_id,
        account_id=current_user.id,
    ).first()
    if recipe is None:
        abort(404)
    db.session().delete(recipe)
    db.session().flush()
    Ingredient.delete_unused_ingredients(current_user.id)
    db.session().commit()
    return redirect(url_for("get_recipes"))
