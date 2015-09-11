#!/usr/bin/env python
# coding: utf-8

"""
sqlalchemy model
"""

import base64
import json
import time

from datetime import datetime
from flask import url_for
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, synonym, backref
from voluptuous import Invalid

from sample import db, login_manager


class Client(db.Model):
    __tablename__ = 'clients'
    # human readable name, not required
    name = db.Column(db.Unicode(40))

    # human readable description, not required
    description = db.Column(db.Unicode(400))

    # creator of the client, not required
    user_id = db.Column(db.Unicode(200))

    client_id = db.Column(db.Unicode(40), primary_key=True)
    client_secret = db.Column(db.Unicode(55), unique=True, index=True, nullable=False)

    # public or confidential
    is_confidential = db.Column(db.Boolean)

    _redirect_uris = db.Column(db.UnicodeText)
    _default_scopes = db.Column(db.UnicodeText)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.Unicode(100), primary_key=True, nullable=False)
    name = db.Column(db.Unicode(200))
    _password = db.Column('password', db.Unicode(100))

    def _get_encrypted_password(self, password):
        from hashlib import sha256

        return sha256(password).hexdigest()

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            password = password.strip()

        self._password = self._get_encrypted_password(password)

    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def check_password(self, password):
        if self.password is None or not password.strip():
            return False

        password = password.strip()
        return self.password == self._get_encrypted_password(password)

    @classmethod
    def authenticate(cls, query, user_id, password):
        user_id = user_id.strip().lower()
        user = query(cls).filter(cls.user_id == user_id).first()
        if user is None:
            return None, False

        return user, user.check_password(password)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.user_id}>'.format(self=self)


class Grant(db.Model):
    __tablename__ = 'grants'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Unicode(200))

    client_id = db.Column(db.Unicode(40), db.ForeignKey('clients.client_id'), nullable=False, )
    client = relationship('Client')

    code = db.Column(db.Unicode(255), index=True, nullable=False)

    redirect_uri = db.Column(db.Unicode(255))
    expires = db.Column(db.DateTime)

    _scopes = db.Column(db.UnicodeText)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.Unicode(40), db.ForeignKey('clients.client_id'),
        nullable=False,
    )
    client = relationship('Client')

    user_id = db.Column(db.Unicode(200))

    # currently only bearer is supported
    token_type = db.Column(db.Unicode(40))

    access_token = db.Column(db.Unicode(255), unique=True)
    refresh_token = db.Column(db.Unicode(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.UnicodeText)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

    def _get_scope(self):
        if self._scopes:
            return self._scopes.split()
        return []

    def _set_scope(self, scope):
        if scope:
            scope = scope
        self._scopes = scope

    scope_descriptor = property(_get_scope, _set_scope)
    scope = synonym('_scopes', descriptor=scope_descriptor)


@login_manager.user_loader
def load_user(user_id):
    """Hook for Flask-Login to load a User instance from a user ID."""
    return User.query.get(user_id)


class BaseMixin(object):
    id = db.Column('id', db.Integer, primary_key=True)
    created_at = db.Column('created_at', db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column('updated_at', db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def get_date_fields(self):
        return dict(
            created_at=self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=self.updated_at.strftime("%Y-%m-%d %H:%M:%S"))
