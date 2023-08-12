from dataclasses import dataclass

__all__ = (
    'ContactDoesNotExistError',
    'ContactAlreadyExistsError',
    'UserDoesNotExistsError',
    'UserAlreadyExistsError',
)


@dataclass(frozen=True, slots=True)
class UserDoesNotExistsError(Exception):
    user_id: int


class UserAlreadyExistsError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class ContactDoesNotExistError(Exception):
    contact_id: int


class ContactAlreadyExistsError(Exception):
    pass
