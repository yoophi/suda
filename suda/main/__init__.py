from flask import Blueprint

main = Blueprint('main', __name__)

from suda.main import views, errors
