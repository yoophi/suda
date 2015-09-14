#!/usr/bin/env python
# coding: utf-8

import os
import os.path as op

from flask import Flask
from flask.ext.babelex import Babel
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
import flask_admin
from flask_admin.contrib import sqla

from sample import config, config_factory
from sample.models import User, Client

template_folder = op.join(op.dirname(op.abspath(__file__)), 'templates')

debug_toolbar = DebugToolbarExtension()

app = Flask(__name__, template_folder=template_folder, )
app.secret_key = 'SECRET'
app.debug = True

config = config_factory(os.getenv('FLASK_CONFIG') or 'default')
debug_toolbar.init_app(app)
config.init_app(app)

db = SQLAlchemy(app)

# Initialize babel
babel = Babel(app, default_locale='ko')


@babel.localeselector
def get_locale():
    return 'ko'


class MyModelView(sqla.ModelView):
    pass


class UserAdmin(MyModelView):
    form_columns = ['username', 'name', 'password']
    column_list = ['username', 'name']


class ClientAdmin(MyModelView):
    form_columns = ['client_id', 'client_secret', 'name', 'description', 'is_confidential', 'redirect_uris_text', 'default_scopes_text']
    column_list = ['client_id', 'name', 'description', 'is_confidential', 'redirect_uris_text', 'default_scopes_text']


admin = flask_admin.Admin(app, template_mode='bootstrap3',
                          translations_path=op.join(op.dirname(__file__), 'translations'))

admin.add_view(UserAdmin(User, db.session))
admin.add_view(ClientAdmin(Client, db.session))


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
