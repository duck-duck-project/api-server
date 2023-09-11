from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from models.transaction_sources import TransactionSource

__all__ = ('Transfer',)


class UserPartial(BaseModel):
    id: int
    username: str | None
    fullname: str


class Transfer(BaseModel):
    id: UUID
    sender: UserPartial
    recipient: UserPartial
    source: TransactionSource
    amount: int
    description: str | None
    created_at: datetime

    class Config:
        use_enum_values = True
