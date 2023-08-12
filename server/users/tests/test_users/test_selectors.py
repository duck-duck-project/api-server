from django.test import TestCase

from users.exceptions import UserDoesNotExistsError
from users.models import User
from users.selectors.users import get_user_by_id


class TestUserSelectors(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            id=123456789,
            username='usbtypec',
            fullname='Eldos',
        )

    def test_get_user_by_id(self) -> None:
        user = get_user_by_id(123456789)
        self.assertEqual(user, self.user)

    def test_get_user_by_id_does_not_exist(self) -> None:
        with self.assertRaises(UserDoesNotExistsError) as error:
            get_user_by_id(12345)
        self.assertEqual(error.exception.user_id, 12345)
