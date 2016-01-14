from wtforms import Form, StringField, PasswordField
from wtforms.validators import required


class LoginForm(Form):
    """Render HTML input for user login form.

    Authentication (i.e. password verification) happens in the view function.
    """
    username = StringField('Username', [required()])
    password = PasswordField('Password', [required()])


class JoinForm(Form):
    """Render HTML input for user join form.

    Authentication (i.e. password verification) happens in the view function.
    """
    username = StringField('Username', [required()])
    password = PasswordField('Password', [required()])
