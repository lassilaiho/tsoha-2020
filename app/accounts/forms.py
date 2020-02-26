from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, PasswordField, validators
from wtforms.fields.html5 import SearchField

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


class GetAccountsForm(FlaskForm):
    query = SearchField("Search", [validators.length(
        max=100,
        message="Query can be at most %(max)d characters",
    )], default="")
    page = IntegerField("Page", default=1)

    def page_clamped(self, min_value=1, max_value=9999999):
        return max(min_value, min(self.page.data, max_value))

    class Meta:
        # CSRF protection isn't needed because this form is only used in GET
        # requests.
        csrf = False
