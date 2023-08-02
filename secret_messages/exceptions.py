from dataclasses import dataclass
from uuid import UUID

__all__ = (
    'ContactDoesNotExistError',
    'ContactAlreadyExistsError',
    'SecretMessageDoesNotExistError',
    'SecretMediaAlreadyExistsError',
    'SecretMediaDoesNotExistError',
)


@dataclass(frozen=True, slots=True)
class ContactDoesNotExistError(Exception):
    contact_id: int


class ContactAlreadyExistsError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class SecretMessageDoesNotExistError(Exception):
    secret_message_id: UUID


@dataclass(frozen=True, slots=True)
class SecretMediaDoesNotExistError(Exception):
    secret_media_id: UUID


class SecretMediaAlreadyExistsError(Exception):
    pass
