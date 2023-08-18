from uuid import UUID

from pydantic import BaseModel

from models.contacts import Contact
from models.secret_media_types import SecretMediaType

__all__ = ('SecretMedia',)


class SecretMedia(BaseModel):
    id: UUID
    file_id: str
    name: str | None
    media_type: SecretMediaType
    contact: Contact
