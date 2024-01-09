from dataclasses import dataclass
from uuid import UUID

__all__ = ('TransactionIsNotTransferError',)


@dataclass(frozen=True, slots=True)
class TransactionIsNotTransferError(Exception):
    transaction_id: UUID

    def __str__(self) -> str:
        return f'Transaction with ID {self.transaction_id} is not a transfer.'
