"""
TestCase migration with Flask-Testing
"""
from flask import url_for
from flask.ext.testing import TestCase

from suda import create_app


class SampleTest(TestCase):
    def create_app(self):
        return create_app('testing')

    def test_main_index(self):
        self.assert200(self.client.get(url_for('main.index')))
