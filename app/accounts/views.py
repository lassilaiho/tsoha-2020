from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user

from app.main import app, bcrypt, db
from app.accounts.models import Account
from app.accounts.forms import LoginForm


def render_login_error():
    return render_template(
        "accounts/login.html",
        form=form,
        error="Invalid username or password",
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("accounts/login.html", form=LoginForm())
    form = LoginForm(request.form)
    if not form.validate():
        return render_template("accounts/login.html", form=form)
    account = Account.query.filter_by(username=form.username.data).first()
    if account is None or \
            not bcrypt.check_password_hash(
                account.password_hash,
                form.password.data,
            ):
        return render_login_error()
    login_user(account)
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("accounts/register.html", form=LoginForm())
    form = LoginForm(request.form)
    if not form.validate():
        return render_template("accounts/register.html", form=form)
    password_hash = bcrypt.generate_password_hash(form.password.data)
    account = Account(form.username.data, password_hash, "user")
    db.session().add(account)
    db.session.commit()
    login_user(account)
    return redirect(url_for("index"))
