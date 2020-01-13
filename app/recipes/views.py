from flask import render_template, url_for, redirect, request

from app.main import app, db
from app.recipes.models import Recipe


@app.route("/recipes")
def get_recipes():
    return render_template(
        "recipes/index.html",
        recipes=Recipe.query.all(),
    )


@app.route("/recipes/new")
def create_recipe_form():
    return render_template(
        "recipes/edit.html",
        form_action=url_for("create_recipe"),
        recipe=Recipe("", "", ""),
    )


@app.route("/recipes/new", methods=["POST"])
def create_recipe():
    recipe = Recipe(
        name=request.form.get("name"),
        description=request.form.get("description"),
        steps=request.form.get("steps"),
    )
    db.session().add(recipe)
    db.session().commit()
    return redirect(url_for("get_recipes"))


@app.route("/recipes/<int:recipe_id>")
def get_recipe(recipe_id: int):
    return render_template(
        "recipes/edit.html",
        form_action=url_for("update_recipe", recipe_id=recipe_id),
        recipe=Recipe.query.get(recipe_id),
    )


@app.route("/recipes/<int:recipe_id>", methods=["POST"])
def update_recipe(recipe_id: int):
    recipe = Recipe.query.get(recipe_id)
    recipe.name = request.form.get("name")
    recipe.description = request.form.get("description")
    recipe.steps = request.form.get("steps")
    db.session().commit()
    return redirect(url_for("get_recipes"))


@app.route("/recipes/<int:recipe_id>/delete", methods=["POST"])
def delete_recipe(recipe_id: int):
    db.session().delete(Recipe.query.get(recipe_id))
    db.session().commit()
    return redirect(url_for("get_recipes"))
