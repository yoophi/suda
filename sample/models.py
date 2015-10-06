#!/usr/bin/env python
# coding: utf-8

"""
sqlalchemy model
"""

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, synonym

db = SQLAlchemy()


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(40))

    # human readable description, not required
    description = db.Column(db.Unicode(400))

    # creator of the client, not required
    user_id = db.Column(db.Unicode(200))

    client_id = db.Column(db.Unicode(40), unique=True)
    client_secret = db.Column(db.Unicode(55), index=True, nullable=False)

    # public or confidential
    is_confidential = db.Column(db.Boolean)

    redirect_uris_text = db.Column(db.UnicodeText)
    default_scopes_text = db.Column(db.UnicodeText)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self.redirect_uris_text:
            return self.redirect_uris_text.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self.default_scopes_text:
            return self.default_scopes_text.split()
        return []

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.Unicode(100), unique=True, nullable=False)
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
    def authenticate(cls, query, username, password):
        username = username.strip().lower()
        user = query(cls).filter(cls.username == username).first()
        if user is None:
            return None, False

        return user, user.check_password(password)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)


class Grant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # user_id = db.Column(db.Unicode(200))dd
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(User.__tablename__ + '.id'),
        nullable=False, )
    user = relationship('User')

    client_id = db.Column(db.Unicode(40), db.ForeignKey(Client.__tablename__ + '.client_id'), nullable=False, )
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
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.Unicode(40),
        db.ForeignKey(Client.__tablename__ + '.client_id'),
        nullable=False,
    )
    client = relationship('Client')

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(User.__tablename__ + '.id'),
        nullable=False, )
    user = relationship('User')

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

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)
