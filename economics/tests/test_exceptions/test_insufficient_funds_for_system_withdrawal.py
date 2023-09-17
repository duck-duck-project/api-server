from django.test import TestCase

from economics.exceptions import InsufficientFundsForSystemWithdrawalError


class InsufficientFundsForSystemWithdrawalErrorStrTests(TestCase):

    def test_str(self) -> None:
        error = InsufficientFundsForSystemWithdrawalError(
            user_id=1,
            amount=2,
            balance=3,
            description='payment',
        )
        self.assertEqual(
            str(error),
            f'User {error.user_id} has insufficient funds for system withdrawal'
            f' of {error.amount}. Balance: {error.balance}.'
            f' Transaction: {error.description}.',
        )
