#!/usr/bin/env python
# coding: utf-8

"""
auth tester
"""

from flask import url_for
from flask.ext.fixtures import load_fixtures

from tests import TesterBase
from suda.models import db
from tests.fixtures.users import dataset


class Tester(TesterBase):
    def test_login(self):
        load_fixtures(db, dataset)

        data = {
            'grant_type': 'password',
            'client_id': 'foo',
            'client_secret': 'secret',
            'username': 'suda@test.com',
            'password': 'secret',
            'scope': 'email'
        }
        status_code, body = self.get(url_for('api.user_access_token'), data)
        self.assertEqual(status_code, 200)
        status_code, body = self.get(url_for('api.me'), headers={
            'Authorization': 'Bearer %s' % (body['access_token'],)
        })
        self.assertEqual(status_code, 200)
        self.assertEqual(body['username'], 'suda@test.com')
        self.assertEqual(body['name'], 'user')

        # 존재하지 않는 토큰 요청
        status_code, body = self.get(url_for('api.me'), headers={
            'Authorization': 'Bearer expect expired'
        })
        self.assertEqual(status_code, 401)
        self.assertEqual(body['message'], 'Bearer token not found.')
