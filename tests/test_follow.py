import json

from flask import url_for
from flask.ext.fixtures import load_fixtures
from flask.ext.testing import TestCase
from sqlalchemy.exc import IntegrityError

from suda import db, create_app
from suda.models import User
from tests import ModelTestCase

dataset = [
    dict(
        model='suda.models.User',
        records=[
            dict(
                id=1,
                username=u'suda@test.com',
                name=u'suda',
                password=u'secret'
            ),
            dict(
                id=2,
                username=u'user1@test.com',
                name=u'user1',
                password=u'secret'
            ),
            dict(
                id=3,
                username=u'user2@test.com',
                name=u'user2',
                password=u'secret'
            ),
            dict(
                id=4,
                username=u'user3@test.com',
                name=u'user3',
                password=u'secret'
            ),
        ]
    ),
    dict(
        model='suda.models.Relationship',
        records=[
            dict(
                user_id=1,
                followed_by_id=2,
            )
        ]
    ),
]


class RelationshipModelTest(ModelTestCase):
    def test_get_followers(self):
        load_fixtures(db, dataset)

        u1 = User.query.get(1)
        u2 = User.query.get(2)

        followers = u1.get_followed_by()
        self.assertEqual(1, len(followers), 'user has one follower')
        self.assertIsInstance(followers[0], User, 'followers is list of <User> instances')
        self.assertEqual(followers[0].id, 2, '<User 2> follows <User 1>')

        followings = u2.get_follows()
        self.assertEqual(1, len(followings), 'user has one following')
        self.assertIsInstance(followings[0], User, 'followings is list of <User> instances')
        self.assertEqual(followings[0].id, 1, '<User 1> follows <User 1>')

    def test_add_follower(self):
        load_fixtures(db, dataset)

        user = User.query.get(1)
        user.add_follower(User.query.get(3))
        db.session.add(user)
        db.session.commit()

        followers = user.get_followed_by()
        self.assertEqual(2, len(followers), 'user has two follower')

        user.add_follower(User.query.get(2))

        with self.assertRaises(IntegrityError):
            db.session.add(user)
            db.session.commit()

        self.assertEqual(2, len(followers), 'user has two follower')

    def test_follow(self):
        load_fixtures(db, dataset)

        user = User.query.get(1)
        self.assertEqual(0, len(user.followings))
        self.assertEqual(0, len(user.get_follows()))

        u2 = User.query.get(2)
        user.follow(u2)

        db.session.add(user)
        db.session.commit()

        self.assertEqual(1, len(user.followings))
        self.assertEqual(1, len(user.get_follows()))
        self.assertEqual(u2, user.get_follows()[0])

        with self.assertRaises(IntegrityError):
            user.follow(u2)
            db.session.add(user)
            db.session.commit()


class RelationshipClientTest(TestCase):
    def create_app(self):
        return create_app('testing')

    def setUp(self):
        super(RelationshipClientTest, self).setUp()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        super(RelationshipClientTest, self).tearDown()

    def test_user_follows(self):
        load_fixtures(db, dataset)

        rv = self.client.get(url_for('api.user_follows', username='suda@test.com'))
        self.assert200(rv)
        self.assertEqual(1, len(json.loads(rv.data)['users']))

    def test_user_followed_by(self):
        load_fixtures(db, dataset)

        rv = self.client.get(url_for('api.user_followed_by', username='suda@test.com'))
        self.assert200(rv)
        self.assertEqual(0, len(json.loads(rv.data)['users']))

        rv1 = self.client.get(url_for('api.user_follows', username='user1@test.com'))
        self.assert200(rv1)
        self.assertEqual(1, len(json.loads(rv1.data)['users']))
