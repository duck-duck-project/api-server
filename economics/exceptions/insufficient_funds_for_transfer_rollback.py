from dataclasses import dataclass
from uuid import UUID

__all__ = ('InsufficientFundsForTransferRollbackError',)


@dataclass(frozen=True, slots=True)
class InsufficientFundsForTransferRollbackError(Exception):
    transaction_id: UUID
