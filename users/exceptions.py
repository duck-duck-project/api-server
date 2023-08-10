from dataclasses import dataclass

__all__ = (
    'ContactDoesNotExistError',
    'ContactAlreadyExistsError',
    'UserDoesNotExistsError',
)


@dataclass(frozen=True, slots=True)
class UserDoesNotExistsError(Exception):
    user_id: int


@dataclass(frozen=True, slots=True)
class ContactDoesNotExistError(Exception):
    contact_id: int


class ContactAlreadyExistsError(Exception):
    pass
