from flask import Blueprint

auth = Blueprint('auth', __name__)

from sample.auth import views
