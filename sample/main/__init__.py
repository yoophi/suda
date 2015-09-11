from flask import Blueprint

main = Blueprint('main', __name__)

from sample.main import views, errors
