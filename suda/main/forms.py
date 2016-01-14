from wtforms import Form, StringField, TextAreaField
from wtforms.validators import required


class PostForm(Form):
    """Render HTML input for user post form.

    """
    title = StringField('Title', [required()])
    body = TextAreaField('Body', [required()])

