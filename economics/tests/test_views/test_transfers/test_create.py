from django.urls import reverse
from rest_framework.test import APITestCase

from economics.models import Transaction
from economics.tests.factories import SystemDepositFactory
from users.tests.test_users.factories import UserFactory


class TransferCreateApiTests(APITestCase):

    def setUp(self) -> None:
        self.alice = UserFactory()
        self.bob = UserFactory()

        SystemDepositFactory(
            recipient=self.alice,
            amount=1000,
        )

    def test_create_transfer(self) -> None:
        url = reverse('economics:transfers-create')
        request_data = {
            'sender_id': self.alice.id,
            'recipient_id': self.bob.id,
            'amount': 100,
            'description': 'Test transfer',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            response.data,
            {
                'id': response.data['id'],
                'sender': {
                    'id': self.alice.id,
                    'username': self.alice.username,
                    'fullname': self.alice.fullname,
                },
                'recipient': {
                    'id': self.bob.id,
                    'username': self.bob.username,
                    'fullname': self.bob.fullname,
                },
                'amount': 100,
                'description': 'Test transfer',
                'created_at': response.data['created_at'],
            },
        )

    def test_create_transfer_insufficient_funds_for_transfer(self) -> None:
        url = reverse('economics:transfers-create')
        request_data = {
            'sender_id': self.alice.id,
            'recipient_id': self.bob.id,
            'amount': 1200,
            'description': 'Test transfer',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], 'Insufficient funds for transfer')

    def test_create_transfer_sender_does_not_exist(self) -> None:
        url = reverse('economics:transfers-create')
        request_data = {
            'sender_id': self.alice.id,
            'recipient_id': 999,
            'amount': 500,
            'description': 'Test transfer',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['detail'], 'User does not exists')

    def test_create_transfer_recipient_does_not_exist(self) -> None:
        url = reverse('economics:transfers-create')
        request_data = {
            'sender_id': 5345,
            'recipient_id': self.bob.id,
            'amount': 500,
            'description': 'Test transfer',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['detail'], 'User does not exists')

    def test_create_transfer_both_users_do_not_exist(self) -> None:
        url = reverse('economics:transfers-create')
        request_data = {
            'sender_id': 5345,
            'recipient_id': 4234234,
            'amount': 500,
            'description': 'Test transfer',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['detail'], 'User does not exists')

    def test_create_transfer_amount_less_than_min_value(self) -> None:
        url = reverse('economics:transfers-create')
        request_data = {
            'sender_id': self.alice.id,
            'recipient_id': self.bob.id,
            'amount': 0,
            'description': 'Test transfer',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data['amount'][0],
            'Amount must be greater than 0',
        )

    def test_create_transfer_amount_greater_than_max_value(self) -> None:
        url = reverse('economics:transfers-create')
        request_data = {
            'sender_id': self.alice.id,
            'recipient_id': self.bob.id,
            'amount': 5001,
            'description': 'Test transfer',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
