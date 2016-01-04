# coding: utf-8

from flask import request
from flask.ext.restful import abort

from sample import oauth, ma
from sample.api_1_0 import api
from sample.models import User


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'name', '_links')

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'user_info': ma.URLFor('api.user_info', username='<username>'),
        # 'collection': ma.URLFor('authors')
    })


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@api.route('/me')
@oauth.require_oauth('email')
def me():
    user = request.oauth.user
    return user_schema.jsonify(user)


@api.route('/user/<username>')
def user_info(username):
    user = User.query.filter(User.username == username).first()
    if not user:
        return abort(404)

    return user_schema.jsonify(user)
