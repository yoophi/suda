#!/usr/bin/env python
# coding: utf-8

import unittest
import json
from flask import url_for
from flask.ext.testing import TestCase

from suda import create_app, db
from tests.utils import load_fixtures_from_file


class TesterBase(unittest.TestCase):
    """
    testing common code
    """

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        # db.engine.connect().connection.connection.text_factory = str
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get(self, url, query_string={}, headers={}):
        rv = self.client.get(url, query_string=query_string, headers=headers)
        return rv._status_code, json.loads(rv.get_data(as_text=True))

    def post(self, url, data='', query_string={}, headers={}, content_type='application/json'):
        rv = self.client.post(url, query_string=query_string, data=data, headers=headers, content_type=content_type)
        if rv._status_code == 200:
            return rv._status_code, json.loads(rv.get_data(as_text=True))
        else:
            return rv._status_code, None

    def get_access_token(self, username='suda@test.com', password='secret'):
        payload = {
            'grant_type': 'password',
            'client_id': 'foo',
            'client_secret': 'secret',
            'username': username,
            'password': password,
            'scope': 'email'
        }
        _, body = self.get(url_for('api.user_access_token'), query_string=payload)
        if 'access_token' not in body:
            raise Exception(body.get('error', None))

        return body['access_token']


class ModelTestCase(TestCase):
    def create_app(self):
        return create_app('testing')

    def setUp(self):
        super(ModelTestCase, self).setUp()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        super(ModelTestCase, self).tearDown()