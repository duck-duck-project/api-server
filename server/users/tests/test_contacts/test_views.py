from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User, Contact


class ContactCreateApiTests(APITestCase):

    def setUp(self) -> None:
        self.eldos = User.objects.create(
            id=123456789,
            username='usbtypec',
            fullname='Eldos',
        )
        self.alex = User.objects.create(
            id=987654321,
            username='pushkin',
            fullname='Alexander Pushkin',
        )

    def test_create_contact(self) -> None:
        url = reverse('users:contacts-create')
        data = {
            'of_user_id': self.eldos.id,
            'to_user_id': self.alex.id,
            'private_name': 'Alex',
            'public_name': 'Alexander',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['of_user']['id'], self.eldos.id)
        self.assertEqual(response.data['to_user']['id'], self.alex.id)
        self.assertIn('id', response.data)

        contact = (
            Contact.objects
            .select_related('of_user', 'to_user')
            .get(id=response.data['id'])
        )

        self.assertEqual(contact.of_user, self.eldos)
        self.assertEqual(contact.to_user, self.alex)
        self.assertEqual(contact.private_name, 'Alex')
        self.assertEqual(contact.public_name, 'Alexander')
        self.assertFalse(contact.is_hidden)

    def test_create_contact_of_user_does_not_exist(self) -> None:
        url = reverse('users:contacts-create')
        data = {
            'of_user_id': 12345,
            'to_user_id': self.alex.id,
            'private_name': 'Alex',
            'public_name': 'Alexander',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_contact_already_exists(self):
        url = reverse('users:contacts-create')
        data = {
            'of_user_id': self.eldos.id,
            'to_user_id': self.alex.id,
            'private_name': 'Alex',
            'public_name': 'Alexander',
        }
        self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data, {'detail': 'Contact already exists'})


class ContactUpdateApiTests(APITestCase):

    def setUp(self) -> None:
        self.eldos = User.objects.create(
            id=123456789,
            username='usbtypec',
            fullname='Eldos',
        )
        self.alex = User.objects.create(
            id=987654321,
            username='pushkin',
            fullname='Alexander Pushkin',
        )
        self.contact = Contact.objects.create(
            of_user=self.eldos,
            to_user=self.alex,
            private_name='Alex',
            public_name='Alexander',
        )

    def test_update_contact(self) -> None:
        url = reverse(
            'users:contacts-retrieve-update-delete',
            args=(self.contact.id,),
        )
        data = {
            'private_name': 'Tom',
            'public_name': 'Hanks',
            'is_hidden': True,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.contact.refresh_from_db()

        self.assertEqual(self.contact.private_name, 'Tom')
        self.assertEqual(self.contact.public_name, 'Hanks')
        self.assertTrue(self.contact.is_hidden)

    def test_update_contact_not_found(self) -> None:
        url = reverse(
            'users:contacts-retrieve-update-delete',
            args=(22,),
        )
        data = {
            'private_name': 'Tom',
            'public_name': 'Hanks',
            'is_hidden': True,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ContactDeleteApiTests(APITestCase):

    def setUp(self) -> None:
        self.eldos = User.objects.create(
            id=123456789,
            username='usbtypec',
            fullname='Eldos',
        )
        self.alex = User.objects.create(
            id=987654321,
            username='pushkin',
            fullname='Alexander Pushkin',
        )
        self.contact = Contact.objects.create(
            of_user=self.eldos,
            to_user=self.alex,
            private_name='Alex',
            public_name='Alexander',
        )

    def test_delete_contact(self) -> None:
        url = reverse(
            'users:contacts-retrieve-update-delete',
            args=(self.contact.id,),
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contact.objects.filter(id=self.contact.id).exists())

    def test_delete_contact_not_found(self) -> None:
        url = reverse(
            'users:contacts-retrieve-update-delete',
            args=(22,),
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ContactRetrieveApiTests(APITestCase):

    def setUp(self) -> None:
        self.eldos = User.objects.create(
            id=123456789,
            username='usbtypec',
            fullname='Eldos',
        )
        self.alex = User.objects.create(
            id=987654321,
            username='pushkin',
            fullname='Alexander Pushkin',
        )
        self.contact = Contact.objects.create(
            of_user=self.eldos,
            to_user=self.alex,
            private_name='Alex',
            public_name='Alexander',
        )

    def test_retrieve_user_by_id(self) -> None:
        url = reverse(
            'users:contacts-retrieve-update-delete',
            args=(self.contact.id,),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.contact.id)
        self.assertEqual(response.data['of_user']['id'], self.eldos.id)
        self.assertEqual(response.data['to_user']['id'], self.alex.id)
        self.assertEqual(response.data['private_name'], 'Alex')
        self.assertEqual(response.data['public_name'], 'Alexander')
        self.assertFalse(response.data['is_hidden'])

    def test_retrieve_user_does_not_exist(self) -> None:
        url = reverse(
            'users:contacts-retrieve-update-delete',
            args=(22,),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Contact does not exist'})


class UserContactsListApiTests(APITestCase):

    def setUp(self) -> None:
        self.eldos = User.objects.create(
            id=123456789,
            username='usbtypec',
            fullname='Eldos',
        )
        self.alex = User.objects.create(
            id=987654321,
            username='pushkin',
            fullname='Alexander Pushkin',
        )
        self.shahadat = User.objects.create(
            id=111111111,
            username=None,
            fullname='Shahadat',
        )
        self.contact1 = Contact.objects.create(
            of_user=self.eldos,
            to_user=self.alex,
            private_name='Alex',
            public_name='Alexander',
        )
        self.contact2 = Contact.objects.create(
            of_user=self.eldos,
            to_user=self.shahadat,
            private_name='Shahadat',
            public_name='Shahadat',
        )

    def test_get_contacts_list(self) -> None:
        url = reverse('users:contacts-list', args=(self.eldos.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_contacts_list_unknown_user_id(self):
        url = reverse('users:contacts-list', args=(432245435,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
