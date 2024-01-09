from dataclasses import dataclass
from uuid import UUID

__all__ = ('TransferSenderDoesNotMatchError',)


@dataclass(frozen=True, slots=True)
class TransferSenderDoesNotMatchError(Exception):
    transaction_id: UUID
    sender_id: int | type[int]

    def __str__(self) -> str:
        return (
            f'Transaction with ID {self.transaction_id} does not belong to '
            f'user with ID {self.sender_id}.'
        )
