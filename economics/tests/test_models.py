from django.core.exceptions import ValidationError
from django.test import TestCase

from economics.models import Transaction
from users.tests.test_users.factories import UserFactory


class TransactionTypeTests(TestCase):

    def setUp(self) -> None:
        self.user = UserFactory()

    def test_is_deposit(self):
        transaction = Transaction(recipient=self.user, amount=100)
        self.assertTrue(transaction.is_deposit)
        self.assertFalse(transaction.is_transfer)
        self.assertFalse(transaction.is_withdrawal)

    def test_is_withdrawal(self):
        transaction = Transaction(sender=self.user, amount=100)
        self.assertTrue(transaction.is_withdrawal)
        self.assertFalse(transaction.is_deposit)
        self.assertFalse(transaction.is_transfer)

    def test_is_transfer(self):
        transaction = Transaction(
            sender=self.user,
            recipient=self.user,
            amount=100,
        )
        self.assertTrue(transaction.is_transfer)
        self.assertFalse(transaction.is_deposit)
        self.assertFalse(transaction.is_withdrawal)


class TransactionConstraintsTests(TestCase):

    def setUp(self) -> None:
        self.user = UserFactory()

    def test_transaction_has_neither_sender_nor_recipient(self):
        with self.assertRaises(ValidationError) as error:
            Transaction(sender=None, recipient=None, amount=100).full_clean()
        self.assertEqual(
            'Transaction must have at least either sender or recipient',
            error.exception.messages[0],
        )

    def test_transaction_to_self(self):
        with self.assertRaises(ValidationError) as error:
            Transaction(
                sender=self.user,
                recipient=self.user,
                amount=100,
            ).full_clean()

        self.assertEqual(
            'Sender and recipient must not be equal',
            error.exception.messages[0],
        )
