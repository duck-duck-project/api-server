from enum import Enum

__all__ = ('TransactionSource',)


class TransactionSource(Enum):
    TRANSFER = 1
    SYSTEM = 2
