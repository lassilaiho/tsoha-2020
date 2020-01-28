from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


class LoginForm(FlaskForm):
    username = StringField("Username", [validators.required()])
    password = PasswordField("Password", [validators.required()])

    class Meta:
        csrf = False


class RegisterForm(LoginForm):
    confirm_password = PasswordField(
        "Confirm Password",
        [validators.equal_to("password", "Passwords must match")],
    )

    class Meta:
        csrf = False


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current password", [validators.input_required()])
    new_password = PasswordField("New password", [validators.input_required()])
    confirm_new_password = PasswordField(
        "Confirm new password",
        [validators.equal_to("new_password", "Passwords must match")],
    )

    class Meta:
        csrf = False
