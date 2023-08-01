from dataclasses import dataclass
from uuid import UUID

__all__ = (
    'ContactDoesNotExistError',
    'ContactAlreadyExistsError',
    'SecretMessageDoesNotExistError',
)


@dataclass(frozen=True, slots=True)
class ContactDoesNotExistError(Exception):
    contact_id: int


class ContactAlreadyExistsError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class SecretMessageDoesNotExistError(Exception):
    secret_message_id: UUID
