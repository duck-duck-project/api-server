from django.test import TestCase

from users.exceptions import UserDoesNotExistsError
from users.models import User
from users.selectors.users import get_user_by_id
from users.tests.test_users.factories import UserFactory


class UserSelectorsTests(TestCase):

    def setUp(self) -> None:
        self.user = UserFactory()

    def test_get_user_by_id(self) -> None:
        user = get_user_by_id(self.user.id)
        self.assertEqual(user, self.user)

    def test_get_user_by_id_does_not_exist(self) -> None:
        with self.assertRaises(UserDoesNotExistsError) as error:
            get_user_by_id(12345)
        self.assertEqual(error.exception.user_id, 12345)
