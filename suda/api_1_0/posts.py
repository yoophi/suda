# coding: utf-8
import json
from flask import jsonify, request
from flask.views import MethodView
from suda import ma, oauth
from suda.api_1_0 import api
from suda.models import db, Post


class PostSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'title', 'body', '_links')

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.post', id='<id>'),
        'collection': ma.URLFor('api.posts')
    })


post_schema = PostSchema()
posts_schema = PostSchema(many=True)


class PostApi(MethodView):
    def get(self, id):
        post = Post.query.get_or_404(id)

        return post_schema.jsonify(post)

    @oauth.require_oauth('email')
    def post(self, id):
        current_user = request.oauth.user
        post = Post.query.get_or_404(id)

        if post.user_id != current_user.id:
            return jsonify(error=True, message='Invalid access'), 401

        payload = json.loads(request.data)

        if payload.get('title'):
            post.title = payload.get('title')

        if payload.get('body'):
            post.body = payload.get('body')

        db.session.commit()

        return jsonify(result='Operate successfully', post=post_schema.dump(post).data)

    @oauth.require_oauth('email')
    def delete(self, id):
        current_user = request.oauth.user
        post = Post.query.get_or_404(id)

        if post.user_id != current_user.id:
            return jsonify(error=True, message='Invalid access'), 401

        db.session.delete(post)
        db.session.commit()

        return jsonify(result='Operate successfully')


class PostListApi(MethodView):
    def get(self):
        posts = Post.query.all()
        result = posts_schema.dump(posts)

        return jsonify(posts=result.data)

    @oauth.require_oauth('email')
    def put(self):
        current_user = request.oauth.user

        payload = json.loads(request.data)
        post = Post(title=payload.get('title'), body=payload.get('body'), user_id=current_user.id)
        db.session.add(post)
        db.session.commit()

        return jsonify(result='Operate successfully',
                       post=post_schema.dump(post).data,
                       )


api.add_url_rule('/post/<int:id>', view_func=PostApi.as_view('post'))
api.add_url_rule('/posts', view_func=PostListApi.as_view('posts'))
