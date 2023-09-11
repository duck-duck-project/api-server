from django.urls import reverse
from rest_framework.test import APITestCase

from economics.models import Transaction
from economics.tests.factories import (
    SystemDepositFactory,
    SystemWithdrawalFactory,
    TransferFactory,
)
from users.tests.test_users.factories import UserFactory


class BalanceRetrieveApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = UserFactory()

    def test_user_has_no_balance(self) -> None:
        url = reverse('economics:balance-retrieve', args=(self.user.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.data,
            {
                'user_id': self.user.id,
                'balance': 0,
            },
        )

    def test_user_has_balance(self) -> None:
        SystemDepositFactory(
            recipient=self.user,
            amount=1000,
        )
        url = reverse('economics:balance-retrieve', args=(self.user.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.data,
            {
                'user_id': self.user.id,
                'balance': 1000,
            },
        )


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
                'source': Transaction.Source.TRANSFER.value,
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
        self.assertEqual(
            response.data['amount'][0],
            'Amount must be less or equal to 5000',
        )


class TransactionListApiTests(APITestCase):

    def setUp(self) -> None:
        self.alice = UserFactory()
        self.bob = UserFactory()

    def test_get_system_deposit_transaction(self) -> None:
        deposit = SystemDepositFactory(
            recipient=self.alice,
            amount=1000,
        )
        url = reverse('economics:transactions-list', args={self.alice.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['transactions']), 1)
        self.assertDictEqual(
            response.data,
            {
                'transactions': [
                    {
                        'id': str(deposit.id),
                        'sender': None,
                        'recipient': {
                            'id': self.alice.id,
                            'username': self.alice.username,
                            'fullname': self.alice.fullname,
                        },
                        'amount': deposit.amount,
                        'description': deposit.description,
                        'source': Transaction.Source.SYSTEM.value,
                        'created_at': f'{deposit.created_at:%Y-%m-%dT%H:%M:%S.%fZ}',
                    },
                ],
                'is_end_of_list_reached': True,
            },
        )

    def test_get_system_withdrawal_transaction(self) -> None:
        deposit = SystemDepositFactory(
            recipient=self.alice,
            amount=1000,
        )
        withdrawal = SystemWithdrawalFactory(
            sender=self.alice,
            amount=100,
        )
        url = reverse('economics:transactions-list', args={self.alice.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['transactions']), 2)
        self.assertDictEqual(
            response.data,
            {
                'transactions': [
                    {
                        'id': str(withdrawal.id),
                        'sender': {
                            'id': self.alice.id,
                            'username': self.alice.username,
                            'fullname': self.alice.fullname,
                        },
                        'recipient': None,
                        'amount': withdrawal.amount,
                        'description': withdrawal.description,
                        'source': Transaction.Source.SYSTEM.value,
                        'created_at': f'{withdrawal.created_at:%Y-%m-%dT%H:%M:%S.%fZ}',
                    },
                    {
                        'id': str(deposit.id),
                        'sender': None,
                        'recipient': {
                            'id': self.alice.id,
                            'username': self.alice.username,
                            'fullname': self.alice.fullname,
                        },
                        'amount': deposit.amount,
                        'description': deposit.description,
                        'source': Transaction.Source.SYSTEM.value,
                        'created_at': f'{deposit.created_at:%Y-%m-%dT%H:%M:%S.%fZ}',
                    },
                ],
                'is_end_of_list_reached': True,
            },
        )

    def test_get_user_transfers(self) -> None:
        deposit = SystemDepositFactory(
            recipient=self.alice,
            amount=1000,
        )
        sent_transfer = TransferFactory(
            sender=self.alice,
            recipient=self.bob,
            amount=400,
            description='First transfer',
        )
        received_transfer = TransferFactory(
            sender=self.bob,
            recipient=self.alice,
            amount=200,
            description='Second transfer',
        )

        url = reverse('economics:transactions-list', args={self.alice.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['transactions']), 3)
        self.assertDictEqual(
            response.data,
            {
                'transactions': [
                    {
                        'id': str(received_transfer.id),
                        'sender': {
                            'id': self.bob.id,
                            'username': self.bob.username,
                            'fullname': self.bob.fullname,
                        },
                        'recipient': {
                            'id': self.alice.id,
                            'username': self.alice.username,
                            'fullname': self.alice.fullname,
                        },
                        'amount': received_transfer.amount,
                        'description': received_transfer.description,
                        'source': Transaction.Source.TRANSFER.value,
                        'created_at': f'{received_transfer.created_at:%Y-%m-%dT%H:%M:%S.%fZ}',
                    },
                    {
                        'id': str(sent_transfer.id),
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
                        'amount': sent_transfer.amount,
                        'description': sent_transfer.description,
                        'source': Transaction.Source.TRANSFER.value,
                        'created_at': f'{sent_transfer.created_at:%Y-%m-%dT%H:%M:%S.%fZ}',
                    },
                    {
                        'id': str(deposit.id),
                        'sender': None,
                        'recipient': {
                            'id': self.alice.id,
                            'username': self.alice.username,
                            'fullname': self.alice.fullname,
                        },
                        'amount': deposit.amount,
                        'description': deposit.description,
                        'source': Transaction.Source.SYSTEM.value,
                        'created_at': f'{deposit.created_at:%Y-%m-%dT%H:%M:%S.%fZ}',
                    },
                ],
                'is_end_of_list_reached': True,
            },
        )
