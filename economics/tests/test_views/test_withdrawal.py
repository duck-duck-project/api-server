from django.urls import reverse
from rest_framework.test import APITestCase

from economics.models import Transaction
from economics.services import compute_user_balance
from economics.tests.factories import SystemDepositFactory
from users.tests.test_users.factories import UserFactory


class WithdrawalCreateApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = UserFactory()

        SystemDepositFactory(
            recipient=self.user,
            amount=2000,
        )

    def test_create_withdrawal_response_structure(self) -> None:
        url = reverse('economics:system-withdrawal-create')
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
            },
        )

    def test_balance_after_multiple_withdrawals(self) -> None:
        url = reverse('economics:system-withdrawal-create')
        request_data = {
            'user_id': self.user.id,
            'amount': 150,
            'description': 'withdrawal 1',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.data['amount'], 150)
        self.assertEqual(compute_user_balance(self.user), 1850)

        request_data = {
            'user_id': self.user.id,
            'amount': 350,
            'description': 'withdrawal 2',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.data['amount'], 350)
        self.assertEqual(compute_user_balance(self.user), 1500)

        request_data = {
            'user_id': self.user.id,
            'amount': 450,
            'description': 'withdrawal 3',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.data['amount'], 450)
        self.assertEqual(compute_user_balance(self.user), 1050)

    def test_create_withdrawal_exists_in_database(self) -> None:
        url = reverse('economics:system-withdrawal-create')
        request_data = {
            'user_id': self.user.id,
            'amount': 150,
            'description': 'withdrawal',
        }
        response = self.client.post(url, request_data, format='json')

        withdrawal = Transaction.objects.order_by('-created_at').first()

        self.assertDictEqual(
            response.data,
            {
                'id': str(withdrawal.id),
                'user': {
                    'id': self.user.id,
                    'username': self.user.username,
                    'fullname': self.user.fullname,
                },
                'amount': 150,
                'description': 'withdrawal',
                'source': Transaction.Source.SYSTEM.value,
                'created_at': withdrawal.created_at.strftime(
                    '%Y-%m-%dT%H:%M:%S.%fZ',
                ),
            }
        )

    def test_create_withdrawal_invalid_amount(self) -> None:
        url = reverse('economics:system-withdrawal-create')

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

    def test_create_withdrawal_user_does_not_exist(self) -> None:
        url = reverse('economics:system-withdrawal-create')
        request_data = {
            'user_id': 100,
            'amount': 100,
            'description': 'test',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['detail'], 'User does not exists')

    def test_user_has_insufficient_funds(self) -> None:
        url = reverse('economics:system-withdrawal-create')
        request_data = {
            'user_id': self.user.id,
            'amount': 5000,
            'description': 'test',
        }
        response = self.client.post(url, request_data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], 'Insufficient funds for withdrawal')
