import secrets

from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user

from app.main import app, bcrypt, db, login_required
from app.accounts.models import Account
from app.accounts.forms import LoginForm, RegisterForm, ChangePasswordForm, EditAccountForm


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
        return render_template(
            "accounts/login.html",
            form=form,
            error="Invalid username or password",
        )
    login_user(account)
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("accounts/register.html", form=RegisterForm())
    form = RegisterForm(request.form)
    if not form.validate():
        return render_template("accounts/register.html", form=form)
    if Account.query.filter_by(username=form.username.data).count() > 0:
        return render_template(
            "accounts/register.html",
            form=form,
            error="Username is already taken.",
        )
    password_hash = \
        bcrypt.generate_password_hash(form.password.data).decode("utf-8")
    account = Account(
        username=form.username.data,
        password_hash=password_hash,
        role="user",
    )
    db.session().add(account)
    db.session.commit()
    login_user(account)
    return redirect(url_for("index"))


@app.route("/my-account")
@login_required
def my_account():
    return render_template(
        "accounts/my-account.html",
        change_password_form=ChangePasswordForm(),
    )


@app.route("/my-account/change-password", methods=["POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if not form.validate():
        return jsonify(error_messages=form.errors), 400
    if not bcrypt.check_password_hash(
            current_user.password_hash,
            form.current_password.data):
        return jsonify(error_messages={
            "current_password": ["Current password is incorrect"],
        }), 400
    current_user.password_hash = \
        bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
    db.session().commit()
    return ""


@app.route("/my-account/delete", methods=["POST"])
@login_required
def delete_my_account():
    db.session().delete(
        Account.query.filter_by(id=current_user.id).first_or_404())
    logout_user()
    db.session().commit()
    return redirect(url_for("index"))


@app.route("/accounts")
@login_required(required_role="admin")
def get_accounts():
    form = EditAccountForm()
    return render_template(
        "accounts/accounts.html",
        form=form,
        accounts=Account.query.all(),
    )


@app.route("/accounts/new", methods=["POST"])
@login_required(required_role="admin")
def create_account():
    form = EditAccountForm()
    if not form.validate():
        return jsonify(error_messages=form.errors), 400
    if Account.query.filter_by(username=form.username.data).count() > 0:
        return jsonify(error_messages={
            "username": ["Username is already taken"],
        }), 400
    if form.password.data:
        password = form.password.data
    else:
        password = secrets.token_urlsafe(64)
    db.session().add(Account(
        username=form.username.data,
        role=form.role.data,
        password_hash=bcrypt.generate_password_hash(password).decode("utf-8"),
    ))
    db.session().commit()
    return ""


@app.route("/accounts/<int:account_id>", methods=["POST"])
@login_required(required_role="admin")
def delete_account(account_id):
    Account.query.filter_by(id=account_id).delete()
    db.session().commit()
    return redirect(url_for("get_accounts"))
