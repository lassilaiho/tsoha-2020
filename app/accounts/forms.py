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
