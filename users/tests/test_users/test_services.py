from django.test import TestCase

from users.exceptions import UserAlreadyExistsError
from users.models import User
from users.services.users import create_user, update_user
from users.tests.test_users.factories import UserFactory


class UserCreateServicesTests(TestCase):

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


class UserUpdateServicesTests(TestCase):

    def setUp(self) -> None:
        self.user = UserFactory()

    def test_update_user(self) -> None:
        is_updated = update_user(
            user_id=self.user.id,
            fullname='Alexander',
            username=None,
            secret_message_theme_id=None,
            can_be_added_to_contacts=False,
            can_receive_notifications=True,
            born_at=None,
            profile_photo_url=None,
        )
        self.assertTrue(is_updated)

        self.user.refresh_from_db()

        self.assertEqual(self.user.fullname, 'Alexander')
        self.assertIsNone(self.user.username)
        self.assertIsNone(self.user.secret_message_theme_id)
        self.assertFalse(self.user.can_be_added_to_contacts)
        self.assertIsNone(self.user.born_at)
        self.assertIsNone(self.user.profile_photo_url)

    def test_update_user_not_found(self) -> None:
        is_updated = update_user(
            user_id=123456788,
            fullname='Alexander',
            username=None,
            secret_message_theme_id=None,
            can_be_added_to_contacts=False,
            can_receive_notifications=True,
            born_at=None,
            profile_photo_url=None,
        )
        self.assertFalse(is_updated)
