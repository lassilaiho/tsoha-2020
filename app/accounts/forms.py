from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, validators

from app.accounts.models import Account


class LoginForm(FlaskForm):
    username = StringField(
        "Username", [validators.required(), validators.length(max=100)])
    password = PasswordField(
        "Password", [validators.required(), validators.length(max=100)])


class RegisterForm(LoginForm):
    confirm_password = PasswordField(
        "Confirm Password",
        [validators.equal_to("password", "Passwords must match"),
         validators.length(max=100)],
    )


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current password", [validators.input_required(), validators.length(max=100)])
    new_password = PasswordField(
        "New password", [validators.input_required(), validators.length(max=100)])
    confirm_new_password = PasswordField(
        "Confirm new password",
        [validators.equal_to(
            "new_password", "Passwords must match"), validators.length(max=100)],
    )


class EditAccountForm(FlaskForm):
    username = StringField(
        "Username", [validators.data_required(), validators.length(max=100)])
    role = SelectField(
        "Role", choices=sorted(map(lambda x: (x, x), Account.valid_roles)))
    password = PasswordField(
        "Password", [validators.optional(), validators.length(max=100)])
