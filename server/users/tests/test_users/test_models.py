from django.test import TestCase

from users.models import User


class UserModelTestCase(TestCase):

    def test_user_str(self):
        user = User(
            fullname='John Doe',
            username='johndoe',
        )
        self.assertEqual(str(user), 'johndoe')

        user = User(
            fullname='John Doe',
            username=None,
        )
        self.assertEqual(str(user), 'John Doe')
