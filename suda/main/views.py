from flask import render_template, request, redirect, url_for
from flask.ext.login import current_user
from suda.main import main
from suda.main.forms import PostForm
from suda.models import Post, db


@main.route('/', methods=['GET', 'POST'])
def index():
    # return 'Hello, %s' % (current_user.email if hasattr(current_user, 'email') else 'world')
    return render_template('index.html')


@main.route('/posts', methods=['GET'])
def posts():
    posts = Post.query.all()
    return render_template('posts/list.html', posts=posts)


@main.route('/post/<int:id>', methods=['GET'])
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('posts/detail.html', post=post)


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


@main.route('/error')
def error():
    return 'ERROR_URI'
