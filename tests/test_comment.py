from suda import db
from suda.models import Post, Comment
from tests import ModelTestCase


class CommentModelTest(ModelTestCase):
    def test_post_comment(self):
        db.session.add(Post(title='hello'))
        db.session.commit()

        post = Post.query.filter(Post.title == 'hello').first()
        self.assertIsNotNone(post)

        self.assertItemsEqual([], post.comments)
        comment_body = 'sample comment'
        post.comments.append(Comment(body=comment_body))

        self.assertEqual(1, len(post.comments))
        self.assertEqual(comment_body, post.comments[0].body)
