# coding: utf-8

from flask import jsonify

from sample import ma
from sample.api_1_0 import api
from sample.models import Post


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


@api.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)

    return post_schema.jsonify(post)


@api.route('/posts')
def posts():
    posts = Post.query.all()
    result = posts_schema.dump(posts)

    return jsonify(posts=result.data)
