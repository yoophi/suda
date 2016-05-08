#!/usr/bin/env python
# coding: utf-8

import os
import click
import shortuuid
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script.commands import ShowUrls
from sqlalchemy.exc import IntegrityError

from suda import create_app, db
from suda.models import Client

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True, include='suda/*')
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


@manager.command
def add_client():
    default_client_secret = shortuuid.uuid()

    name = click.prompt('name')
    client_id = click.prompt('client_id')
    client_secret = click.prompt('client_secret', default=default_client_secret,
                                 hide_input=True, confirmation_prompt=True)
    description = click.prompt('description', default='sample client')
    is_confidential = click.prompt('is_confidential', default=False, type=bool)
    redirect_uris = click.prompt('redirect_uri', )
    scopes = click.prompt('scopes', )

    client = Client(
        client_id=client_id,
        client_secret=client_secret,
        name=name,
        description=description,
        is_confidential=is_confidential,
        redirect_uris_text=redirect_uris,
        default_scopes_text=scopes,
    )

    db.session.add(client)
    try:
        db.session.commit()
    except IntegrityError as e:
        click.echo('Error occurred while add client: <%s>' % client_id)
        db.session.rollback()
    finally:
        print client


manager.add_command('shell', Shell(make_context=make_shell_context, use_bpython=True))
manager.add_command('db', MigrateCommand)
manager.add_command('show_urls', ShowUrls)

if __name__ == '__main__':
    manager.run()
