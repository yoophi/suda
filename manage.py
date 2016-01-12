#!/usr/bin/env python
# coding: utf-8

import os

from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script.commands import ShowUrls

from sample import create_app, db

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True, include='sample/*')
    COV.start()

app = create_app(os.getenv('FLASK_CONFIG') or 'development')

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


@manager.command
def test(coverage=False):
    """Run the unit test."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys

        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print 'Coverage Summary:'
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print 'HTML version: file://%s/index.html' % (covdir,)
        COV.erase()


manager.add_command('shell', Shell(make_context=make_shell_context, use_bpython=True))
manager.add_command('db', MigrateCommand)
manager.add_command('show_urls', ShowUrls)

if __name__ == '__main__':
    manager.run()
