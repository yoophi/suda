#!/usr/bin/env python
# coding: utf-8
import os.path as op

from flask.ext.cors import CORS
from flask.ext.login import LoginManager
from flask.ext.oauthlib.provider import OAuth2Provider

from .helpers import Flask
from .models import db, User

__version__ = '0.1'

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

oauth = OAuth2Provider()
cors = CORS()

def create_app(config_name):
    """
    :param config_name: developtment, production or testing
    :return: flask application

    flask application generator
    """
    template_folder = op.join(op.dirname(op.abspath(__file__)), 'templates')
    app = Flask(__name__, template_folder=template_folder)
    app.config.from_yaml(app.root_path)
    app.config.from_heroku()

    cors.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    oauth.init_app(app)

    from sample.main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from sample.auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from sample.api_1_0 import api as api_1_0_blueprint

    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app


@login_manager.user_loader
def load_user(user_id):
    """Hook for Flask-Login to load a User instance from a user ID."""
    return User.query.get(user_id)
