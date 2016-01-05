from flask import render_template, request, redirect, url_for
from flask.ext.login import current_user
from sample.main import main
from sample.main.forms import PostForm
from sample.models import Post, db


@main.route('/', methods=['GET', 'POST'])
def index():
    # return 'Hello, %s' % (current_user.email if hasattr(current_user, 'email') else 'world')
    return render_template('index.html')


@main.route('/posts', methods=['GET'])
def posts():
    posts = Post.query.all()
    return render_template('posts/list.html', posts=posts)


@main.route('/post/add', methods=['GET', 'POST'])
def post_add():
    form = PostForm(request.form)

    if request.method == 'POST' and form.validate():
        title = form.title.data.lower().strip()
        body = form.body.data.lower().strip()
        post = Post(title=title, body=body)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.posts'))

    return render_template('posts/add.html', form=form)
