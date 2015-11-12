#!/usr/bin/env python
# coding: utf-8

import os
import os.path as op
import sys
import logging

from ConfigParser import SafeConfigParser

basedir = op.abspath(op.dirname(__file__))


class Config(object):
    section_name = None

    BUNDLE_ERRORS = True
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or "SECRET_KEY"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_BINDS = {}

    def __init__(self):
        if not self.section_name:
            return

        candidates = [
            op.join(op.dirname(basedir), 'config.ini'),
            '/etc/sample/config.ini',
        ]

        parser = SafeConfigParser()
        parser.read(candidates)
        if not parser.has_section(self.section_name):
            import logging
            logging.warning('no section [%s]' % self.section_name)
            sys.exit(1)

        for key, value in parser.items(self.section_name):
            key = str(key).upper()
            setattr(self, key, value)

            if key.startswith('SQLALCHEMY_BINDS_'):
                self.SQLALCHEMY_BINDS[key.replace('SQLALCHEMY_BINDS_', '').lower()] = value

    def init_app(self, app):
        app.config.from_object(self)


class TestConfig(Config):
    section_name = 'testing'

    SERVER_NAME = 'localhost'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///:memory:'
    SQLALCHEMY_BINDS = {
        'adtv_user': 'sqlite:///:memory:',
        'integrate': 'sqlite:///:memory:'
    }
    TESTING = True


class DevelopmentConfig(Config):
    section_name = 'development'


class ProductionConfig(Config):
    section_name = 'production'

    DEBUG = False


def config_factory(config_name='default'):
    config = {'development': DevelopmentConfig, 'testing': TestConfig, 'production': ProductionConfig,
              'default': DevelopmentConfig}

    return config[config_name]()
