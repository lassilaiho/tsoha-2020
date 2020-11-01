from flask import Response, render_template, send_file
from flask_login import current_user
from werkzeug.exceptions import HTTPException

from app.main import app, login_required
from app.accounts.models import Account
from app.recipes.models import Recipe
from app.shopping_list.models import ShoppingListItem


@app.route("/")
@login_required
def index():
    if app.config["SHOW_TOP_COLLECTORS"]:
        top_collectors = Account.get_top_recipe_collectors(5)
    else:
        top_collectors = None
    return render_template(
        "index.html",
        item_count=ShoppingListItem.query.filter_by(
            account_id=current_user.id).count(),
        recipe_count=Recipe.query.filter_by(
            account_id=current_user.id).count(),
        top_collectors=top_collectors,
    )


@app.route("/manifest.json")
def app_manifest():
    return Response("""{
        "name": "Recipe Book",
        "icons": [
            {
                "src": "/static/img/icon-192.png",
                "type": "image/png",
                "sizes": "192x192"
            },
            {
                "src": "/static/img/icon-512.png",
                "type": "image/png",
                "sizes": "512x512"
            }
        ],
        "start_url": "/",
        "display": "standalone",
        "shortcuts": [
            {
                "name": "Recipes",
                "url": "/recipes"
            },
            {
                "name": "Add Recipe",
                "url": "/recipes/new"
            },
            {
                "name": "Shopping List",
                "url": "/shopping-list"
            }
        ]
    }""", mimetype="application/json")


@app.route("/serviceWorker.js")
def service_worker():
    return send_file("static/js/serviceWorker.js")


@app.errorhandler(HTTPException)
def handle_404(error):
    if error.code == 404:
        return render_template("error-404.html")
    return render_template("error-generic.html", error=error)
