# coding: utf-8

from flask import request, jsonify
from flask.ext.restful import abort
from suda import oauth, ma
from suda.api_1_0 import api
from suda.api_1_0.posts import posts_schema
from suda.models import User


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


@api.route('/me/posts')
@oauth.require_oauth('email')
def my_post_list():
    user = request.oauth.user

    result = posts_schema.dump(user.posts)

    return jsonify(posts=result.data)


@api.route('/user/<username>')
def user_info(username):
    user = User.query.filter(User.username == username).first()
    if not user:
        return abort(404)

    return user_schema.jsonify(user)


@api.route('/user/<username>/posts')
def user_post_list(username):
    user = User.query.filter(User.username == username).first()
    if not user:
        return abort(404)

    result = posts_schema.dump(user.posts)

    return jsonify(posts=result.data)
