import os
from functools import wraps

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import event, engine

from app.config import DefaultConfig, load_config

app = Flask(__name__)

app.config.from_object(DefaultConfig)
app.config.update(load_config())

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

app.config["SECRET_KEY"] = os.urandom(32)

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in."


def login_required(_func=None, *, required_role="user"):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not (current_user and current_user.is_authenticated):
                return login_manager.unauthorized()
            if not current_user.fullfills_role(required_role):
                return login_manager.unauthorized()
            return func(*args, **kwargs)
        return decorated_view
    return wrapper if _func is None else wrapper(_func)


def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
    event.listen(engine.Engine, "connect", enable_sqlite_foreign_keys)
