from django.test import TestCase

from economics.exceptions import InsufficientFundsForTransferError


class InsufficientFundsForTransferErrorStrTests(TestCase):

    def test_str(self) -> None:
        error = InsufficientFundsForTransferError(
            sender_id=1,
            sender_balance=100,
            recipient_id=2,
            transfer_amount=200,
        )
        self.assertEqual(
            str(error),
            f'User {error.sender_id} has insufficient funds for transfer of'
            f' {error.transfer_amount} to user {error.recipient_id}.',
        )
