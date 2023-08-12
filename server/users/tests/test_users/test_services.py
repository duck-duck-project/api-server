from django.test import TestCase

from users.exceptions import UserAlreadyExistsError
from users.models import User
from users.services.users import create_user, update_user


class TestUserCreateServices(TestCase):

    def test_create_user(self) -> None:
        user = create_user(
            user_id=123456789,
            username='usbtypec',
            fullname='Eldos',
        )
        self.assertEqual(user, User.objects.get(id=123456789))

    def test_create_user_already_exists(self) -> None:
        User.objects.create(
            id=123456789,
            username='usbtypec',
            fullname='Eldos',
        )
        with self.assertRaises(UserAlreadyExistsError):
            create_user(
                user_id=123456789,
                username='usbtypec',
                fullname='Eldos',
            )


class TestUserUpdateServices(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            id=123456789,
            username='usbtypec',
            fullname='Eldos',
        )

    def test_update_user(self) -> None:
        is_updated = update_user(
            user_id=123456789,
            fullname='Alexander',
            username=None,
            secret_message_theme_id=None,
            can_be_added_to_contacts=False,
            is_premium=True,
        )
        self.assertTrue(is_updated)

        self.user.refresh_from_db()

        self.assertEqual(self.user.fullname, 'Alexander')
        self.assertIsNone(self.user.username)
        self.assertIsNone(self.user.secret_message_theme_id)
        self.assertFalse(self.user.can_be_added_to_contacts)
        self.assertTrue(self.user.is_premium)

    def test_update_user_not_found(self) -> None:
        is_updated = update_user(
            user_id=123456788,
            fullname='Alexander',
            username=None,
            secret_message_theme_id=None,
            can_be_added_to_contacts=False,
            is_premium=True,
        )
        self.assertFalse(is_updated)
