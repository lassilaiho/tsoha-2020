from importlib import import_module

from app.main import app, db

import_module("app.main")
import_module("app.views")
import_module("app.recipes.models")
import_module("app.recipes.views")
import_module("app.accounts.models")
import_module("app.accounts.views")
import_module("app.ingredients.models")
import_module("app.shopping_list.models")
import_module("app.shopping_list.views")

db.create_all()
