from django.test import TestCase

from economics.exceptions import InsufficientFundsForTransferError
from economics.services import create_transfer
from economics.tests.factories import SystemDepositFactory
from users.tests.test_users.factories import UserFactory


class TransferCreateServicesTests(TestCase):

    def setUp(self) -> None:
        self.alice = UserFactory()
        self.bob = UserFactory()
        SystemDepositFactory(
            recipient=self.alice,
            amount=1000,
        )

    def test_create_transfer(self):
        transfer = create_transfer(
            sender=self.alice,
            recipient=self.bob,
            amount=800,
        )
        self.assertEqual(transfer.sender, self.alice)
        self.assertEqual(transfer.recipient, self.bob)
        self.assertEqual(transfer.amount, 800)

    def test_create_transfer_with_insufficient_balance(self):
        with self.assertRaises(InsufficientFundsForTransferError):
            create_transfer(
                sender=self.alice,
                recipient=self.bob,
                amount=1200,
            )
