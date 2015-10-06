from flask import render_template
from flask.ext.login import current_user

from sample.main import main


@main.route('/', methods=['GET', 'POST'])
def index():
    # return 'Hello, %s' % (current_user.email if hasattr(current_user, 'email') else 'world')
    return render_template('index.html')

