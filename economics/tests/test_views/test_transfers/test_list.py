from django.urls import reverse
from rest_framework.test import APITestCase

from economics.models import Transaction
from economics.tests.factories import (
    SystemDepositFactory,
    TransferFactory,
    SystemWithdrawalFactory,
)
from users.tests.test_users.factories import UserFactory


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
