from flask import Blueprint

auth = Blueprint('auth', __name__)

from suda.auth import views
