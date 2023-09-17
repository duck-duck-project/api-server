from django.test import TestCase

from economics.services import compute_user_balance
from economics.tests.factories import (
    SystemDepositFactory,
    SystemWithdrawalFactory,
    TransferFactory,
)
from users.tests.test_users.factories import UserFactory


class ComputeUserBalanceTests(TestCase):

    def setUp(self) -> None:
        self.alice = UserFactory()
        self.bob = UserFactory()

        SystemDepositFactory(
            recipient=self.alice,
            amount=1000,
        )
        SystemDepositFactory(
            recipient=self.bob,
            amount=100,
        )

    def test_balance_after_system_deposit(self) -> None:
        SystemDepositFactory(
            recipient=self.alice,
            amount=500,
        )
        self.assertEqual(compute_user_balance(self.alice), 1500)

    def test_balance_after_system_withdrawal(self) -> None:
        SystemWithdrawalFactory(
            sender=self.alice,
            amount=400
        )
        self.assertEqual(compute_user_balance(self.alice), 600)

    def test_balance_after_transfer_to_user(self) -> None:
        TransferFactory(
            sender=self.alice,
            recipient=self.bob,
            amount=50
        )
        self.assertEqual(compute_user_balance(self.alice), 950)
        self.assertEqual(compute_user_balance(self.bob), 150)

    def test_balance_after_transfer_from_user(self) -> None:
        TransferFactory(
            sender=self.bob,
            recipient=self.alice,
            amount=50
        )
        self.assertEqual(compute_user_balance(self.alice), 1050)
        self.assertEqual(compute_user_balance(self.bob), 50)
