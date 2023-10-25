from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from economics.models import OperationPrice
from economics.tests.factories import SystemDepositFactory
from users.models import User, Contact
from users.tests.test_contacts.factories import ContactFactory
from users.tests.test_users.factories import UserFactory


class ContactCreateApiTests(APITestCase):

    def setUp(self) -> None:
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()

    def test_create_contact_insufficient_funds(self) -> None:
        url = reverse('users:contacts-create')
        data = {
            'of_user_id': self.user_1.id,
            'to_user_id': self.user_2.id,
            'private_name': 'Alex',
            'public_name': 'Alexander',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data['detail']),
            'Insufficient funds for contact creation',
        )
        self.assertEqual(
            int(response.data['amount']),
            OperationPrice.CREATE_CONTACT,
        )

    def test_create_contact_already_exists(self) -> None:
        SystemDepositFactory(
            recipient=self.user_1,
            amount=OperationPrice.CREATE_CONTACT,
        )
        contact = ContactFactory(of_user=self.user_1, to_user=self.user_2)
        data = {
            'of_user_id': contact.of_user.id,
            'to_user_id': contact.to_user.id,
            'private_name': contact.private_name,
            'public_name': contact.public_name,
        }
        url = reverse('users:contacts-create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            str(response.data['detail']),
            'Contact already exists',
        )

    def test_create_contact(self) -> None:
        SystemDepositFactory(recipient=self.user_1, amount=1000)
        url = reverse('users:contacts-create')
        data = {
            'of_user_id': self.user_1.id,
            'to_user_id': self.user_2.id,
            'private_name': 'Alex',
            'public_name': 'Alexander',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['of_user']['id'], self.user_1.id)
        self.assertEqual(response.data['to_user']['id'], self.user_2.id)
        self.assertIn('id', response.data)

        contact = (
            Contact.objects
            .select_related('of_user', 'to_user')
            .get(id=response.data['id'])
        )

        self.assertEqual(contact.of_user, self.user_1)
        self.assertEqual(contact.to_user, self.user_2)
        self.assertEqual(contact.private_name, 'Alex')
        self.assertEqual(contact.public_name, 'Alexander')
        self.assertFalse(contact.is_hidden)

    def test_create_contact_of_user_does_not_exist(self) -> None:
        url = reverse('users:contacts-create')
        data = {
            'of_user_id': 12345,
            'to_user_id': self.user_2.id,
            'private_name': 'Alex',
            'public_name': 'Alexander',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ContactCreateSoftDeletedContactTests(APITestCase):

    def test_create_contact_mark_as_not_deleted(self) -> None:
        contact = ContactFactory(is_deleted=True)
        SystemDepositFactory(recipient=contact.of_user, amount=1000)
        url = reverse('users:contacts-create')
        data = {
            'of_user_id': contact.of_user.id,
            'to_user_id': contact.to_user.id,
            'private_name': 'Alex',
            'public_name': 'Alexander',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], contact.id)
        self.assertEqual(
            response.data['of_user']['id'],
            contact.of_user.id,
        )
        self.assertEqual(
            response.data['to_user']['id'],
            contact.to_user.id,
        )
        self.assertFalse(response.data['is_hidden'])


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
            args=(434,),
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
        self.contact = ContactFactory()

    def test_delete_contact(self) -> None:
        url = reverse(
            'users:contacts-retrieve-update-delete',
            args=(self.contact.id,),
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Contact.objects.get(id=self.contact.id).is_deleted)

    def test_delete_contact_not_found(self) -> None:
        url = reverse(
            'users:contacts-retrieve-update-delete',
            args=(12321324,),
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ContactRetrieveApiTests(APITestCase):

    def setUp(self) -> None:
        self.contact = ContactFactory()

    def test_retrieve_user_by_id(self) -> None:
        url = reverse(
            'users:contacts-retrieve-update-delete',
            args=(self.contact.id,),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.contact.id)
        self.assertEqual(
            response.data['of_user']['id'],
            self.contact.of_user.id,
        )
        self.assertEqual(
            response.data['to_user']['id'],
            self.contact.to_user.id,
        )
        self.assertEqual(
            response.data['private_name'],
            self.contact.private_name,
        )
        self.assertEqual(response.data['public_name'], self.contact.public_name)
        self.assertFalse(response.data['is_hidden'])

    def test_retrieve_user_does_not_exist(self) -> None:
        url = reverse(
            'users:contacts-retrieve-update-delete',
            args=(4312,),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Contact does not exist'})


class UserContactsListApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = UserFactory()
        self.contact_1 = ContactFactory(of_user=self.user)
        self.contact_2 = ContactFactory(of_user=self.user)

    def test_get_contacts_list(self) -> None:
        url = reverse('users:contacts-list', args=(self.user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_contacts_list_unknown_user_id(self):
        url = reverse('users:contacts-list', args=(432245435,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
