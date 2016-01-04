from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

from sample.api_1_0 import authentication, users, posts


@api.route('/sample')
def do_sample():
    return jsonify({'result': 'sample'})
