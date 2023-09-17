from django.core.exceptions import ValidationError
from django.test import TestCase

from economics.models import Transaction
from users.tests.test_users.factories import UserFactory


class SystemTransactionValidationTests(TestCase):

    def setUp(self) -> None:
        self.alice = UserFactory()
        self.bob = UserFactory()

    def test_system_transaction_has_sender(self) -> None:
        transaction = Transaction(
            sender=self.alice,
            amount=100,
            source=Transaction.Source.SYSTEM,
        )
        transaction.full_clean()
        transaction.save()

        self.assertTrue(Transaction.objects.filter(id=transaction.id).exists())

    def test_system_transaction_has_recipient(self) -> None:
        transaction = Transaction(
            recipient=self.bob,
            amount=100,
            source=Transaction.Source.SYSTEM,
        )
        transaction.full_clean()
        transaction.save()

        self.assertTrue(Transaction.objects.filter(id=transaction.id).exists())

    def test_system_transaction_has_not_sender_nor_recipient(self) -> None:
        transaction = Transaction(
            amount=100,
            source=Transaction.Source.SYSTEM,
        )
        with self.assertRaisesMessage(
                expected_exception=ValidationError,
                expected_message=(
                        'System transaction must have'
                        ' either sender or recipient'
                ),
        ):
            transaction.full_clean()

    def test_system_transaction_has_both_sender_and_recipient(self) -> None:
        transaction = Transaction(
            sender=self.alice,
            recipient=self.bob,
            amount=100,
            source=Transaction.Source.SYSTEM,
        )
        with self.assertRaisesMessage(
                expected_exception=ValidationError,
                expected_message=(
                        'System transaction can not have both'
                        ' sender and recipient'
                ),
        ):
            transaction.full_clean()


class TransferTransactionValidationTests(TestCase):

    def setUp(self) -> None:
        self.alice = UserFactory()
        self.bob = UserFactory()

    def test_transfer_transaction_has_both_sender_and_recipient(self) -> None:
        transaction = Transaction(
            sender=self.alice,
            recipient=self.bob,
            amount=100,
            source=Transaction.Source.TRANSFER,
        )
        transaction.full_clean()
        transaction.save()

        self.assertTrue(Transaction.objects.filter(id=transaction.id).exists())

    def test_transfer_transaction_has_no_sender(self) -> None:
        transaction = Transaction(
            recipient=self.bob,
            amount=100,
            source=Transaction.Source.TRANSFER,
        )
        with self.assertRaisesMessage(
                expected_exception=ValidationError,
                expected_message=(
                        'Transfer transaction must have'
                        ' both sender and recipient'
                ),
        ):
            transaction.full_clean()

    def test_transfer_transaction_has_no_recipient(self) -> None:
        transaction = Transaction(
            sender=self.alice,
            amount=100,
            source=Transaction.Source.TRANSFER,
        )
        with self.assertRaisesMessage(
                expected_exception=ValidationError,
                expected_message=(
                        'Transfer transaction must have'
                        ' both sender and recipient'
                ),
        ):
            transaction.full_clean()

    def test_transaction_transaction_has_not_sender_nor_recipient(self) -> None:
        transaction = Transaction(
            amount=100,
            source=Transaction.Source.TRANSFER,
        )
        with self.assertRaisesMessage(
                expected_exception=ValidationError,
                expected_message=(
                        'Transfer transaction must have'
                        ' both sender and recipient'
                ),
        ):
            transaction.full_clean()
