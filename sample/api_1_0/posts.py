# coding: utf-8
import json
from flask import jsonify, request
from sample import ma
from sample.api_1_0 import api
from sample.models import db, Post


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


@api.route('/post', methods=['PUT'])
def post_add():
    data = json.loads(request.data)
    post = Post(title=(data['title']), body=(data['body']))
    db.session.add(post)
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return post_schema.jsonify(post)
