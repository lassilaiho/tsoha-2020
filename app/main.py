import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

from app.config import load_config

app = Flask(__name__)

app.config.from_object("app.config.DefaultConfig")
app.config.update(load_config())

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

app.config["SECRET_KEY"] = os.urandom(32)

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in."
