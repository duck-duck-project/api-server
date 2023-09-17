from dataclasses import dataclass
from uuid import UUID

__all__ = (
    'SecretMessageDoesNotExistError',
    'SecretMediaAlreadyExistsError',
    'SecretMediaDoesNotExistError',
    'ThemeDoesNotExistError',
)


@dataclass(frozen=True, slots=True)
class SecretMessageDoesNotExistError(Exception):
    secret_message_id: UUID


@dataclass(frozen=True, slots=True)
class SecretMediaDoesNotExistError(Exception):
    secret_media_id: UUID


class SecretMediaAlreadyExistsError(Exception):
    pass


class ThemeDoesNotExistError(Exception):
    pass
