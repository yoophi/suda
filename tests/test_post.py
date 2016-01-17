from suda import db
from suda.models import Post
from tests import ModelTestCase


class PostModelTest(ModelTestCase):
    def test_post_list(self):
        self.assertItemsEqual([], Post.query.all())

        db.session.add(Post(title='hello'))
        db.session.commit()

        self.assertEqual(1, len(Post.query.all()))
