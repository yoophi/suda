# coding: utf-8

from flask import request, jsonify
from sample.api_1_0 import api
from sample import oauth


@api.route('/me')
@oauth.require_oauth('email')
def me():
    user = request.oauth.user
    return jsonify(id=user.id, username=user.username)


