from flask import render_template, url_for, redirect, request, abort
from flask_login import login_required

from app.main import app, db
from app.recipes.models import Recipe
from app.recipes.forms import EditRecipeForm


def render_edit_form(action, form):
    return render_template(
        "recipes/edit.html",
        form_action=action,
        form=form,
    )


@app.route("/recipes")
@login_required
def get_recipes():
    return render_template(
        "recipes/index.html",
        recipes=Recipe.query.all(),
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
    db.session().add(recipe)
    db.session().commit()
    return redirect(url_for("get_recipes"))


@app.route("/recipes/<int:recipe_id>")
@login_required
def get_recipe(recipe_id: int):
    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        abort(404)
    form = EditRecipeForm()
    form.name.data = recipe.name
    form.description.data = recipe.description
    form.steps.data = recipe.steps
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
    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        abort(404)
    recipe.name = form.name.data
    recipe.description = form.description.data
    recipe.steps = form.steps.data
    db.session().commit()
    return redirect(url_for("get_recipes"))


@app.route("/recipes/<int:recipe_id>/delete", methods=["POST"])
@login_required
def delete_recipe(recipe_id: int):
    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        abort(404)
    db.session().delete(recipe)
    db.session().commit()
    return redirect(url_for("get_recipes"))
