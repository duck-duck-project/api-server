from uuid import UUID

from pydantic import BaseModel

__all__ = ('SecretMessage',)


class SecretMessage(BaseModel):
    id: UUID
    text: str
