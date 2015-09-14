#!/usr/bin/env python
# coding: utf-8

"""
oauth implementation
"""

from datetime import datetime, timedelta
from flask import request, render_template, jsonify, redirect
from flask.ext.login import current_user, login_required

from sample.api_1_0 import api
from sample import oauth, db
from sample.models import Client, Grant, User, Token


@oauth.clientgetter
def load_user_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


@oauth.grantgetter
def load_user_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()


def get_current_user():
    return User.query.get(current_user.id)


@oauth.grantsetter
def save_user_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user_id=get_current_user().id,
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant


@oauth.tokengetter
def load_user_token(access_token=None, refresh_token=None):
    if access_token:
        tok = Token.query.filter_by(access_token=access_token).first()
        if tok and tok.user_id:
            tok.user = User.query.get(tok.user_id)
        return tok
    elif refresh_token:
        tok = Token.query.filter_by(refresh_token=refresh_token).first()
        if tok and tok.user_id:
            tok.user = User.query.get(tok.user_id)
        return tok


@oauth.tokensetter
def save_user_token(token, request, *args, **kwargs):
    expires_in = token.pop('expires_in') + 60*60
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(**token)
    tok.expires = expires
    tok.client_id = request.client.client_id

    if not request.user:
        tok.user_id = current_user.id
    else:
        tok.user_id = request.user.id

    db.session.add(tok)
    db.session.commit()
    return tok


@oauth.usergetter
def get_user(username, password, *args, **kwargs):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None


@api.route('/oauth/authorize', methods=['GET', 'POST'])
@login_required
@oauth.authorize_handler
def user_authorize(*args, **kwargs):
    user = get_current_user()
    if not user:
        return redirect('/')

    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        kwargs['user'] = user
        return render_template('authorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'


@api.route('/oauth/token', methods=['GET', 'POST'])
@oauth.token_handler
def user_access_token():
    """
    .. http:get:: /oauth/token
    .. http:post:: /oauth/token

    인증

    **Example request**:

    .. sourcecode:: http

       POST /oauth/token HTTP/1.1
       Host: example.com
       Content-Type: application/json

       {
          'grant_type': 'password',
          'client_id': 'foo',
          'client_secret': 'secret',
          'username': 'sample@test.com',
          'password': 'secret',
          'scope': 'email'
       }

    **Example response**:

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Vary: Accept
       Content-Type: application/json

       {
         "access_token": "AoIgDdA2m1QQOM2jrdOhgnQbCZHAad",
         "token_type": "Bearer",
         "refresh_token": "Z27qmkLmGSIJXBAH9q3aedVJqKJRow",
         "scope": "email"
       }

    **AccessToken이 만료된 경우 응답**

    .. sourcecode:: http

       HTTP/1.1 401 UNAUTHORIZED

       {
         "message": "Bearer token is expired."
       }

    **RefreshToken이 삭제된 경우의 응답 (또는 존재하지 않는 경우)**
        - 다음 경우에는 user_id, password 이용해서 다시 access_token을 발급 받아야 함. (Guest 경우에는 user_id, device_id 조합)

    .. sourcecode:: http

       HTTP/1.1 401 UNAUTHORIZED

       {
         "error": "invalid_grant."
       }
    """
    return None


@oauth.invalid_response
def invalid_require_oauth(req):
    return jsonify(message=req.error_message), 401
