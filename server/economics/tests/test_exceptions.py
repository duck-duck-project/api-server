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
            'User 1 has insufficient funds for transfer of 200 to user 2.',
        )
