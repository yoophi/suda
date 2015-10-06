from flask import render_template, redirect, request, url_for
from flask.ext.login import login_user, logout_user, current_user
from sample.auth import auth
from sample.models import db, User
from sample.auth.forms import LoginForm, JoinForm


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('main.index'))
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        email = form.username.data.lower().strip()
        password = form.password.data.lower().strip()
        user, authenticated = User.authenticate(db.session.query, email, password)
        if authenticated:
            login_user(user)
            return redirect(request.args.get("next") or url_for("main.index"))
        else:
            error = 'Incorrect username or password. Try again.'
    return render_template('user/login.html', form=form, error=error)


@auth.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/join/', methods=['GET', 'POST'])
def join():
    if current_user.is_authenticated():
        return redirect(url_for('main.index'))

    form = JoinForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        username = form.username.data.lower().strip()
        password = form.password.data.lower().strip()
        # user, authenticated = User.authenticate(db.session.query, email, password)
        # if authenticated:
        #     login_user(user)
        #     return redirect(request.args.get("next") or url_for("main.index"))
        # else:
        #     error = 'Incorrect username or password. Try again.'
        user = User(username=username, name=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('user/join.html', form=form)