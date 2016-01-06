import os
import pprint
from flask.ext.fixtures import load_fixtures
from flask.ext.fixtures.loaders import load


def load_fixtures_from_file(db, filename):
    current_dir = os.path.dirname(__file__)
    filepath = os.path.join(current_dir, 'fixtures', filename)
    return load_fixtures(db, load(filepath))


def dump(data):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(data)
