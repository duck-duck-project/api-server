from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from users.tests.test_users.factories import UserFactory


class UserUpdateApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = UserFactory()

    def test_update_user(self) -> None:
        url = reverse('users:retrieve-update', args=(self.user.id,))
        data = {
            'username': 'pushkin',
            'fullname': 'Alexander Pushkin',
            'can_be_added_to_contacts': False,
            'secret_message_theme_id': None,
            'can_receive_notifications': False,
            'born_at': '2004-10-07',
            'profile_photo_url': 'https://example.com/pushkin.jpg',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.user.refresh_from_db()

        self.assertEqual(self.user.username, 'pushkin')
        self.assertEqual(self.user.fullname, 'Alexander Pushkin')
        self.assertFalse(self.user.can_be_added_to_contacts, False)
        self.assertIsNone(self.user.secret_message_theme_id)
        self.assertFalse(self.user.can_receive_notifications)
        self.assertEqual(self.user.born_on, date(2004, 10, 7))

    def test_update_user_not_found(self) -> None:
        url = reverse('users:retrieve-update', args=(12345,))
        data = {
            'username': 'pushkin',
            'fullname': 'Alexander Pushkin',
            'is_premium': True,
            'can_be_added_to_contacts': False,
            'secret_message_theme_id': None,
            'can_receive_notifications': False,
            'born_at': '2004-10-07',
            'profile_photo_url': 'https://example.com/pushkin.jpg'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserRetrieveApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = UserFactory()

    def test_retrieve_user(self) -> None:
        url = reverse('users:retrieve-update', args=(self.user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'id': self.user.id,
                'fullname': self.user.fullname,
                'username': self.user.username,
                'can_be_added_to_contacts': self.user.can_be_added_to_contacts,
                'secret_message_theme': self.user.secret_message_theme_id,
                'profile_photo_url': self.user.profile_photo_url,
                'is_banned': self.user.is_banned,
                'can_receive_notifications': self.user.can_receive_notifications,
                'born_at': self.user.born_on,
            },
        )

    def test_retrieve_user_does_not_exist(self) -> None:
        url = reverse('users:retrieve-update', args=(12345,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserCreateApiTests(APITestCase):

    def test_create_user(self) -> None:
        data = {
            'id': 123456789,
            'username': 'usbtypec',
            'fullname': 'Eldos',
        }
        url = reverse('users:create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                'id': 123456789,
                'username': 'usbtypec',
                'fullname': 'Eldos',
                'can_be_added_to_contacts': True,
                'secret_message_theme': None,
                'profile_photo_url': None,
                'is_banned': False,
                'can_receive_notifications': True,
                'born_at': None,
            },
        )

    def test_create_user_username_none(self) -> None:
        data = {
            'id': 123456789,
            'username': None,
            'fullname': 'Eldos',
        }
        url = reverse('users:create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                'id': 123456789,
                'username': None,
                'fullname': 'Eldos',
                'can_be_added_to_contacts': True,
                'secret_message_theme': None,
                'profile_photo_url': None,
                'is_banned': False,
                'can_receive_notifications': True,
                'born_at': None,
            },
        )

    def test_create_user_already_exists(self) -> None:
        data = {
            'id': 123456789,
            'username': None,
            'fullname': 'Eldos',
        }
        url = reverse('users:create')
        self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
