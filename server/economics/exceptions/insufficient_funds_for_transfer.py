from dataclasses import dataclass

__all__ = ('InsufficientFundsForTransferError',)


@dataclass(frozen=True, slots=True)
class InsufficientFundsForTransferError(Exception):
    sender_id: int
    sender_balance: int
    recipient_id: int
    transfer_amount: int

    def __str__(self) -> str:
        return (
            f'User {self.sender_id} has insufficient funds'
            f' for transfer of {self.transfer_amount}'
            f' to user {self.recipient_id}.'
        )
