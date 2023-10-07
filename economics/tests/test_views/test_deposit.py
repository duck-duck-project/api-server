from django.urls import reverse
from rest_framework.test import APITestCase

from economics.models import Transaction
from economics.services import compute_user_balance
from users.tests.test_users.factories import UserFactory


class DepositCreateApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = UserFactory()

    def test_create_deposit_response_structure(self) -> None:
        url = reverse('economics:system-deposit-create')
        request_data = {
            'user_id': self.user.id,
            'amount': 100,
            'description': 'test',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.status_code, 201)

        self.assertIn('id', response.data)
        self.assertIn('created_at', response.data)

        response.data.pop('id')
        response.data.pop('created_at')

        self.assertDictEqual(
            response.data,
            {
                'user': {
                    'id': self.user.id,
                    'username': self.user.username,
                    'fullname': self.user.fullname,
                },
                'amount': 100,
                'description': 'test',
                'source': Transaction.Source.SYSTEM.value,
            }
        )

    def test_balance_after_multiple_deposits(self) -> None:
        url = reverse('economics:system-deposit-create')
        request_data = {
            'user_id': self.user.id,
            'amount': 150,
            'description': 'deposit 1',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.data['amount'], 150)
        self.assertEqual(compute_user_balance(self.user), 150)

        request_data = {
            'user_id': self.user.id,
            'amount': 350,
            'description': 'deposit 2',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.data['amount'], 350)
        self.assertEqual(compute_user_balance(self.user), 500)

        request_data = {
            'user_id': self.user.id,
            'amount': 450,
            'description': 'deposit 3',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.data['amount'], 450)
        self.assertEqual(compute_user_balance(self.user), 950)

    def test_create_deposit_exists_in_database(self) -> None:
        url = reverse('economics:system-deposit-create')
        request_data = {
            'user_id': self.user.id,
            'amount': 150,
            'description': 'deposit',
        }
        response = self.client.post(url, request_data, format='json')

        deposit = Transaction.objects.order_by('-created_at').first()

        self.assertDictEqual(
            response.data,
            {
                'id': str(deposit.id),
                'user': {
                    'id': self.user.id,
                    'username': self.user.username,
                    'fullname': self.user.fullname,
                },
                'amount': 150,
                'description': 'deposit',
                'source': Transaction.Source.SYSTEM.value,
                'created_at': deposit.created_at.strftime(
                    '%Y-%m-%dT%H:%M:%S.%fZ',
                ),
            }
        )

    def test_create_deposit_invalid_amount(self) -> None:
        url = reverse('economics:system-deposit-create')

        for amount, error_message in (
                (-100, 'Amount must be greater than 0'),
                (0, 'Amount must be greater than 0'),
        ):
            request_data = {
                'user_id': self.user.id,
                'amount': amount,
                'description': 'test',
            }
            response = self.client.post(url, request_data, format='json')

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.data['amount'][0], error_message)

    def test_create_deposit_user_does_not_exist(self) -> None:
        url = reverse('economics:system-deposit-create')
        request_data = {
            'user_id': 100,
            'amount': 100,
            'description': 'test',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['detail'], 'User does not exists')
