from flask import Blueprint

api = Blueprint('api', __name__)

from suda.api_1_0 import authentication, samples, posts, users
